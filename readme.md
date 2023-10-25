
# Stock Price Prediction System with MLOps using ZenML

## Introduction
I've developed a comprehensive Stock Price Prediction System that integrates the principles of MLOps using the ZenML framework. Throughout this project, my primary goal was to ensure reproducibility, automation,in my ML workflows.

## System Flow and Design

### 1. Data Acquisition
I set up an automated system to periodically fetch stock data from a specific API, ensuring my model always trains on up-to-date data.

### 2. Data Management with RabbitMQ
After fetching the stock data, I utilized RabbitMQ—a robust open-source message broker—to seamlessly feed this data into the subsequent stages of the system. The choice of RabbitMQ was informed by its efficiency in handling large data volumes and its established reputation for ensuring a consistent data flow.

### 3. Data Storage in MySQL
For storage, I chose MySQL because of its proven scalability, reliability, and performance. This database serves as a centralized data repository that simplifies both data management and retrieval.

### 4. Data Visualization with Streamlit
I've integrated a Streamlit dashboard that presents both historical and forecasted stock data, offering users an intuitive platform to glean insights from stock trends.

### 5. Continuous Training and Deployment
In alignment with MLOps principles, I've implemented continuous training to ensure my model dynamically adapts to new data. This guarantees more accurate predictions. Once trained, the updated model is deployed swiftly, minimizing latency between model iterations and real-world application.

### 6. Experiment Tracking with MLflow
For comprehensive versioning and tracking of my model experiments, artifacts, and versions, I've brought in MLflow. This tool ensures a systematic approach to experimentation and underpins reproducibility.

## Why ZenML and MLOps Principles?
The essence of this project is not just stock price prediction, but achieving this systematically. By integrating ZenML, I've added layers of reproducibility and automation to the process. This ensures my ML operations are transparent, trackable, and consistent across varied environments. By adhering to MLOps principles, my ML workflows are designed to be efficient, scalable, and sustainable in the long run.

## Reflections
This system was crafted with a focus on resilience and scalability. I've emphasized MLOps principles, ensuring continuous training, continuous delployment (CT/CD), and model versioning . This makes the entire pipeline adaptive and robust. My choice of tools, especially MySQL and RabbitMQ, stems from the need for efficient data handling, scalability, and reliable performance.

## System diagram

![Architecture](https://github.com/Ariq154404/Mlops-stock-price-prediction/blob/main/assets/system_design.png)

##  Sample dashboard
The streamlit dasboard continusly runs and displays forcasted data from the service and the historical data coming from the mysql database 
![Dashboard](https://github.com/Ariq154404/Mlops-stock-price-prediction/blob/main/assets/dashboard.png)



 




## Pipeline overview
There are main three pipelines for my project 
### 1. CT_CD_pipeline.py
This pipeline is resposible of continuos training and continoud deployment .
![CT_CD_pipeline](https://github.com/Ariq154404/Mlops-stock-price-prediction/blob/main/assets/CTCD.png)

The model and the artifact is tracked and and logged in Mlflow like below:
![mlflow_ct_cd](https://github.com/Ariq154404/Mlops-stock-price-prediction/blob/main/assets/Mlflow.png)

### 2. ETL_pipeline.py
The diagram below depicts the etl pipeline that fethces data from api and dumps into mysql
![ETL](https://github.com/Ariq154404/Mlops-stock-price-prediction/blob/main/assets/ETL.png)


### 3. EDA_pipeline.py
the diagram below depicts the Exploratory Data Analytics pipeline that ocassionlly on a scheduled basis pulls data from from the data base and displays statistical information found in the time series data like seasonality, trend e.t.c

![EDA](https://github.com/Ariq154404/Mlops-stock-price-prediction/blob/main/assets/EDA.png)








## Run Locally

Clone the project

```bash
  git clone https://github.com/Ariq154404/Mlops-stock-price-prediction
```

Create the virtual environment

```bash
  python3 -m venv myenv
```

Activate the virtual Environment

```bash
  source myenv/bin/activate
```

Install the dependencies

```bash
  pip install -r requirements.txt
```

Go to the data engineeing folder 

```bash
  cd data-engineeing
```

Run docker compose to start mysql and rabbit mq and go back to the main directory

```bash
  python3 filter_info.py
  cd ..
```

Set up zenml
```bash
zenml init
zenml integration install mlflow -y
zenml stack register quickstart -a default\
                                -o default\
                                -e mlflow
zenml model-deployer register mlflow --flavor=mlflow
zenml stack update quickstart -d mlflow
zenml model-registry register mlflow --flavor=mlflow
zenml stack update quickstart -d mlflow

```

Run ETL
```bash
pyhon run_ETL_pipeline.py
```
Run CTCD pipeline
```bash
pyhon run_CTCD_pipeline.py
```
Prop The  Mlflow display if you want

```bash
mlflow ui --backend-store-uri $MLFLOW_TRACKING_URI
```
Go to zenml dashboard and see pipelines
```bash
zenml up
```
Run EDA pipeline
```bash
pyhon run_EDA_pipeline.py
```
Now Finally run the dashboard
```bash
streamlit run dashboard.py
```










## Environment Variables

###TODO



## Tech Stack

**Broker**  RabbitMQ

**Database:**  MYSQL

**MLops**  Zenml, Mlflow

**Model**  Facebook prophet

**FrontEnd** Streamlit

