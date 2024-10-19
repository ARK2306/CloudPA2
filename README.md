# Distributed IoT Data Processing System

## Project Overview

This project implements a distributed system for processing IoT sensor data using Apache Kafka, Docker, and machine learning components. The system is designed to run on multiple virtual machines (VMs) in a cloud environment, specifically Chameleon Cloud. The project uses Ansible for automated deployment and configuration management.

## System Architecture

The system consists of the following main components:

1. IoT Data Producer
2. Apache Kafka Message Broker
3. ML Inference Service
4. Database for storing results

These components are distributed across multiple VMs, with Kafka serving as the central message broker.

## Key Components

### 1. IoT Data Producer (`producer(IOT).py`)

- Simulates IoT devices sending image data
- Uses the CIFAR-100 dataset to generate sample images
- Sends images to a Kafka topic for processing
- Implements a producer-consumer pattern to handle message publishing and result consumption

### 2. ML Inference Service (`model.py`)

- Provides a Flask-based API for image classification
- Uses a pre-trained ResNet50 model for inference
- Receives images from Kafka, processes them, and sends results back to Kafka

### 3. Database Updater (`updateDB.py` and `db_inf.py`)

- Consumes messages from Kafka containing original images and inference results
- Updates a PostgreSQL database with the received data

### 4. Kafka Setup

- Uses Apache Kafka 2.13-3.8.0
- Configured for distributed operation across multiple VMs

## Deployment and Configuration

The project uses Ansible for automated deployment and configuration. Key playbooks include:

1. `playbook_master.yaml`: The main playbook that orchestrates the entire deployment process
2. `playbook_create_vms.yaml`: Creates VMs on Chameleon Cloud
3. `playbook_install_packages.yaml`: Installs necessary software packages on VMs
4. `playbook_install_docker.yml`: Installs and configures Docker on VMs
5. `playbook_install_kafka.yaml`: Installs and configures Apache Kafka
6. `playbook_set_firewalld_rules.yaml`: Configures firewall rules for Kafka and other services

## VM Configuration

The project uses four VMs:

1. Team21_vm1
2. Team21_vm2
3. Team21_vm3
4. Team21_vm4

Each VM is configured with:

- Ubuntu 22.04 LTS
- 2 vCPUs
- 3.9 GB RAM
- 40 GB storage

## Network Configuration

- VMs are connected to a private network (192.168.5.0/24)
- Firewall rules are set to allow Kafka (9092, 9093) and Zookeeper (2181) traffic

## Data Flow

1. IoT Producer generates image data and sends it to Kafka
2. ML Inference Service consumes image data, performs classification
3. Inference results are sent back to Kafka
4. Database updater consumes both original data and inference results, storing them in PostgreSQL

# Distributed IoT Data Processing System

[Previous content remains the same up to the "Future Improvements" section]

## Dockerization

The project components have been containerized using Docker to ensure consistency across different environments and to facilitate easier deployment and scaling. The following components have been dockerized:

1. IoT Data Producer
2. ML Inference Service
3. Database Updater (Consumer)

Each component has its own Dockerfile, which specifies the base image, required dependencies, and runtime configuration. The Dockerfiles are designed to create lightweight, production-ready containers.

## Docker Compose

A `docker-compose.yml` file has been created to orchestrate the deployment of all components, including:

- Zookeeper
- Kafka
- IoT Data Producer
- ML Inference Service
- Database Updater
- PostgreSQL database

The Docker Compose file defines the services, their dependencies, environment variables, and network configurations. This allows for easy deployment of the entire system with a single command.

## Scaling Producers for CDF Curve

To generate the Cumulative Distribution Function (CDF) curve, the system supports scaling the number of producers from 1 to 4. This is achieved using Docker Compose's scaling feature. By adjusting the number of producer instances, you can analyze the system's performance under different load conditions.

The process for scaling producers involves:

1. Modifying the `docker-compose.yml` file to allow for multiple producer instances
2. Using the `--scale` option when running `docker-compose up` to specify the desired number of producers
3. Running the system with 1, 2, 3, and 4 producers to collect performance data

## CDF Curve Generation

The Cumulative Distribution Function (CDF) curve is generated by measuring the end-to-end latency for each message processed by the system. The process involves:

1. Collecting latency data from each run with different numbers of producers
2. Processing the collected data to calculate the cumulative distribution
3. Generating a graph that shows the CDF curves for each producer configuration (1 to 4 producers)

The CDF curve provides valuable insights into the system's performance characteristics, including:

- Median latency
- 90th and 95th percentile latencies
- Overall latency distribution

## Monitoring and Logging

- The system uses Python's logging module for application-level logging
- Docker logs can be used for container-level monitoring
- Kafka's built-in monitoring tools can be used for message broker health and performance

## Security Considerations

- Firewall rules are implemented to restrict access to Kafka and other services
- SSH key-based authentication is used for VM access
- Kafka security features (e.g., SSL encryption, SASL authentication) should be considered for production use

## Scalability

The system is designed to be scalable:

- Multiple IoT Producers can be added to increase data ingestion
- Kafka can be scaled by adding more brokers
- ML Inference Service can be horizontally scaled by deploying more instances

## Future Improvements

1. Implement Kafka security features (SSL, SASL)
2. Add monitoring and alerting system (e.g., Prometheus and Grafana)
3. Implement data retention and archiving policies
4. Enhance ML model with periodic retraining capabilities
5. Implement a web-based dashboard for real-time data visualization

## Conclusion

This distributed IoT data processing system demonstrates a scalable architecture for handling large volumes of sensor data. By leveraging technologies like Kafka, Docker, and cloud VMs, it provides a flexible foundation for real-world IoT applications with machine learning capabilities.

## Documentation of Effort Expended (Learning Curve)

The development of this distributed IoT data processing system involved a significant learning curve and effort across various technologies and concepts. This section outlines the major areas of learning and the approximate time invested in each.

### 1. Docker and Containerization

- Understanding containerization concepts and benefits
- Learning Docker basics: images, containers, Dockerfiles
- Developing Dockerfiles for each component of the system
- Using Docker Compose for multi-container applications
- Managing container networking and data persistence

### 2. Machine Learning Integration

- Refreshing knowledge on machine learning concepts and image classification
- Integrating a pre-trained ResNet50 model into the system
- Developing a Flask API for the ML inference service
- Handling image data in a distributed system

### 3. Ansible and Infrastructure as Code

- Learning Ansible basics: playbooks, roles, and inventories
- Developing Ansible playbooks for automated deployment
- Managing secrets and environment-specific configurations

### 4. Performance Testing and Analysis

- Understanding performance metrics for distributed systems
- Implementing latency measurement in the producer and consumer components
- Learning to generate and interpret Cumulative Distribution Function (CDF) curves
- Developing scripts for data collection and visualization

### 5. System Integration and Troubleshooting

- Integrating all components into a cohesive system
- Debugging issues across distributed components
- Ensuring data consistency and handling failure scenarios
- Fine-tuning system parameters for optimal performance

### 6. Documentation and Project Management

- Maintaining project documentation throughout development
- Using version control (Git) effectively for collaborative development
- Managing project timelines and deliverables

### Key Challenges and Learning Outcomes:

1. **Distributed Systems Complexity**: Understanding and managing the complexities of a distributed system, including data consistency, fault tolerance, and scalability.

2. **Kafka Learning Curve**: Kafka's concepts and optimal use required significant study and practical experience to implement effectively.

3. **Cloud Environment Management**: Adapting to cloud-based development and deployment presented initial challenges but provided valuable experience in cloud computing.

4. **Containerization Best Practices**: Learning to create efficient, secure, and scalable containerized applications took time but greatly improved deployment consistency.

5. **Performance Optimization**: Understanding and optimizing the performance of a distributed system required deep dives into each component and their interactions.

6. **Integrating Diverse Technologies**: Combining cloud services, Kafka, Docker, machine learning, and databases into a cohesive system was challenging but highly educational.

The effort expended on this project not only resulted in a functional distributed IoT data processing system but also provided invaluable experience in cutting-edge technologies and practices in the field of distributed systems and cloud computing.



# Distributed IoT Data Processing System

## Team Work Split

The development of this distributed IoT data processing system was a collaborative effort shared equally among three team members: Aryan, Athish, and Alex. Each member took primary responsibility for specific components of the system while also contributing to overall design, integration, and testing. Here's a breakdown of the primary responsibilities:

### Aryan's Responsibilities:

1. **Cloud Infrastructure Setup using Ansible**

   - Setting up and managing Chameleon Cloud resources

2. **Database Design and Integration**

   - Designing the PostgreSQL database schema
   - Implementing database operations in the consumer

3. **Ansible Playbooks**

   - Developing Ansible playbooks for automated deployment
   - Managing configuration files and environment variables

4. **Integration and System Testing**
   - Coordinating integration of all components
   - Conducting end-to-end system testing

### Athish's Responsibilities:

1. **IoT Data Producer**

   - Developing the simulated IoT data producer
   - Implementing Kafka producer logic in Python
   - Handling data serialization and error handling

2. **Apache Kafka Cluster**

   - Designing and implementing the Kafka cluster architecture
   - Configuring Kafka for optimal performance

3. **Docker Containerization**

   - Creating Dockerfiles for all components
   - Developing the docker-compose configuration

4. **Performance Monitoring**
   - Implementing performance metrics collection
   - Developing scripts for CDF curve generation

### Alex's Responsibilities:

1. **ML Inference Service**

   - Integrating the pre-trained ResNet50 model
   - Developing the Flask API for the inference service
   - Optimizing ML model performance

2. **Kafka Consumer Logic**

   - Implementing Kafka consumer logic for processing messages
   - Handling message deserialization and error recovery

3. **Data Visualization**

   - Developing data visualization scripts for system metrics
   - Creating dashboards for monitoring system performance

4. **Documentation**
   - Maintaining project documentation
   - Creating user guides and API documentation

### Shared Responsibilities:

1. **Code Review**

   - Regular code reviews were conducted by all team members to ensure code quality and knowledge sharing

2. **Troubleshooting and Debugging**

   - All members participated in identifying and resolving issues across the system

3. **Performance Optimization**

   - Collaborative effort in identifying bottlenecks and optimizing system performance

4. **Project Management**
   - Rotating responsibility for sprint planning and task allocation
   - Regular team meetings for progress updates and issue resolution

### Work Distribution:

The work was distributed to ensure that each team member had exposure to various aspects of the system while also leveraging individual strengths. The distribution aimed to balance the workload and complexity across the team.

This collaborative approach allowed the team to efficiently develop a complex distributed system while fostering individual growth and a comprehensive understanding of the entire system among all team members.

