from flask import Flask, request, jsonify
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
import numpy as np
from PIL import Image
import io
import base64
from kafka import KafkaProducer
import json
import logging
import os

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
model = ResNet50(weights='imagenet')

KAFKA_BROKER = os.getenv('KAFKA_BROKER', '192.168.5.33:9092')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'team21')
INFERENCE_RESULT_TOPIC = os.getenv('INFERENCE_RESULT_TOPIC', 'inference_result')

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def process_image(image_base64):
    try:
        logging.debug(f"Received image data. Length: {len(image_base64)}")
        logging.debug(f"First 100 chars: {image_base64[:100]}")
        
        image_bytes = base64.b64decode(image_base64)
        logging.debug(f"Decoded base64. Length: {len(image_bytes)}")
        
        image = Image.open(io.BytesIO(image_bytes))
        logging.debug(f"Opened image. Size: {image.size}, Mode: {image.mode}")
        
        image = image.resize((224, 224))  # ResNet50 input size
        image_array = np.array(image)
        image_array = np.expand_dims(image_array, axis=0)
        return preprocess_input(image_array)
    except Exception as e:
        logging.error(f"Error in process_image: {str(e)}")
        raise

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        logging.debug(f"Received data: {data}")
        
        unique_id = data.get('unique_id') or data.get('image_id')
        image_data = data['image']
        
        if not unique_id:
            raise ValueError("Missing 'unique_id' or 'image_id' in request data")
        
        logging.debug(f"Processing request for image {unique_id}")
        
        processed_image = process_image(image_data)
        predictions = model.predict(processed_image)
        decoded_predictions = decode_predictions(predictions, top=1)[0]
        
        inferred_value = decoded_predictions[0][1]
        
        kafka_message = {
            'unique_id': unique_id,
            'inferred_value': inferred_value
        }
        
        # Send to both topics
        producer.send(KAFKA_TOPIC, kafka_message)
        producer.send(INFERENCE_RESULT_TOPIC, kafka_message)
        
        logging.info(f"Processed image {unique_id}. Inferred value: {inferred_value}")
        
        return jsonify(kafka_message)
    except Exception as e:
        logging.error(f"Error in predict: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)