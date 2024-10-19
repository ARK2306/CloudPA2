import threading
import time
from kafka import KafkaProducer, KafkaConsumer
import json
import base64
import numpy as np
from PIL import Image
import tensorflow as tf
import io
import csv
import os

# Load CIFAR-100 dataset
(_, _), (x_test, y_test) = tf.keras.datasets.cifar100.load_data()

# Kafka configuration
KAFKA_BROKER = os.getenv('KAFKA_BROKER', '192.168.5.33:9092')
PUBLISH_TOPIC = os.getenv('PUBLISH_TOPIC', 'team21')
INFERENCE_TOPIC = os.getenv('INFERENCE_TOPIC', 'inference_result')

# Configuration
TOTAL_SAMPLES = int(os.getenv('TOTAL_SAMPLES', '1000'))
SAMPLE_FREQUENCY = float(os.getenv('SAMPLE_FREQUENCY', '1'))  # 1 sample per second

class ProducerConsumer:
    def __init__(self, producer_id):
        self.producer_id = producer_id
        self.producer = KafkaProducer(bootstrap_servers=[KAFKA_BROKER])
        self.consumer = KafkaConsumer(
            INFERENCE_TOPIC,
            bootstrap_servers=[KAFKA_BROKER],
            auto_offset_reset='latest',
            enable_auto_commit=True,
            group_id=f'producer_consumer_{producer_id}',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        self.sent_samples = {}
        self.lock = threading.Lock()
        self.sample_count = 0
        self.results = []
        self.is_producing = True

    def produce(self):
        while self.sample_count < TOTAL_SAMPLES:
            idx = np.random.randint(0, len(x_test))
            image = x_test[idx]
            label = y_test[idx][0]

            img = Image.fromarray(image)
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

            unique_id = f"{self.producer_id}_{int(time.time() * 1000)}_{idx}"
            message = {
                'unique_id': unique_id,
                'image': img_base64,
                'ground_truth': int(label)
            }

            self.producer.send(PUBLISH_TOPIC, json.dumps(message).encode('utf-8'))

            with self.lock:
                self.sent_samples[unique_id] = time.time()
                self.sample_count += 1

            time.sleep(SAMPLE_FREQUENCY)

        self.is_producing = False

    def consume(self):
        while self.is_producing or self.sent_samples:
            for message in self.consumer:
                try:
                    result = message.value
                    unique_id = result.get('unique_id')

                    with self.lock:
                        sent_time = self.sent_samples.pop(unique_id, None)

                    if sent_time:
                        end_to_end_time = time.time() - sent_time
                        print(f"Sample {unique_id}: End-to-end time = {end_to_end_time:.4f} seconds")
                        self.results.append((unique_id, end_to_end_time))

                    if not self.is_producing and not self.sent_samples:
                        break

                except Exception as e:
                    print(f"Error processing message: {e}")

            if not self.is_producing and not self.sent_samples:
                break

    def save_results(self):
        filename = f'latency_results_producer_{self.producer_id}.csv'
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Sample ID', 'Latency (seconds)'])
            for result in self.results:
             writer.writerow(result)
        print(f"Results saved to: {os.path.abspath(filename)}")

    def run(self):
        producer_thread = threading.Thread(target=self.produce)
        consumer_thread = threading.Thread(target=self.consume)

        producer_thread.start()
        consumer_thread.start()

        producer_thread.join()
        consumer_thread.join()

        self.save_results()

def run_producers(num_producers):
    producers = [ProducerConsumer(i) for i in range(1, num_producers + 1)]
    threads = [threading.Thread(target=p.run) for p in producers]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    num_producers = int(os.getenv('NUM_PRODUCERS', '1'))
    print(f"Running with {num_producers} producer(s)...")
    run_producers(num_producers)
    print(f"Finished running with {num_producers} producer(s).")