from kafka import KafkaConsumer
import json
import psycopg2
import base64
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

consumer = KafkaConsumer(
    'team21',
    bootstrap_servers=['192.168.5.33:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

conn = psycopg2.connect(
    dbname="team21_data",
    user="team21user",
    password="team21",
    host="localhost"
)
cur = conn.cursor()

def insert_or_update_data(data):
    try:
        if 'unique_id' in data and 'ground_truth' in data and 'image' in data:
            # This is the original image data
            image_id = data['unique_id']
            ground_truth = data['ground_truth']
            image_data = base64.b64decode(data['image'])
            
            cur.execute("""
                INSERT INTO iot_image_data (unique_id, ground_truth, data)
                VALUES (%s, %s, %s)
                ON CONFLICT (unique_id) 
                DO UPDATE SET
                    ground_truth = EXCLUDED.ground_truth,
                    data = EXCLUDED.data
            """, (image_id, ground_truth, psycopg2.Binary(image_data)))
            logging.info(f"Inserted/Updated original data for image {image_id}")
        
        elif 'unique_id' in data and 'inferred_value' in data:
            # This is the inference result
            image_id = data['unique_id']
            inferred_value = data['inferred_value']
            
            cur.execute("""
                UPDATE iot_image_data
                SET inferred_value = %s
                WHERE unique_id = %s
            """, (inferred_value, image_id))
            logging.info(f"Updated inference result for image {image_id}")
        
        else:
            logging.warning(f"Received message with unexpected format: {data}")
        
        conn.commit()
    except Exception as e:
        logging.error(f"Error processing data: {e}")
        conn.rollback()

try:
    for message in consumer:
        data = message.value
        logging.debug(f"Received message: {data}")
        insert_or_update_data(data)
except KeyboardInterrupt:
    logging.info("Stopping the consumer...")
finally:
    cur.close()
    conn.close()
    consumer.close()