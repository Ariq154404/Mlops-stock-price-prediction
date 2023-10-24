commands
 ```bash
    minikube start driver=docker
    python3.9 -m venv myenv
    source myenv/bin/activate
    cd data-engineering
    docker exec -it data-engineering_mysql_1 mysql -uroot -pmy-secret-pw
    SHOW DATABASES;
    USE stocks;
    SHOW TABLES;
    streamlit run dashboard.py
    docker build -t prophet_forecaster .
    docker run -p 5001:5000 prophet_forecaster
    zenml integration install mlflow -y
    zenml stack register quickstart -a default\
                                 -o default\
                                 -e mlflow
    mlflow ui --backend-store-uri "file:/Users/ariqrahman/Library/Application Support/zenml/local_stores/c5c46e6d-2b8b-45b2-a922-69f62de537c9/mlruns"
    zenml model-deployer register mlflow --flavor=mlflow
    zenml stack update quickstart -d mlflow
    export MLFLOW_TRACKING_URI="file:/Users/ariqrahman/Library/Application Support/zenml/local_stores/c5c46e6d-2b8b-45b2-a922-69f62de537c9/mlruns"
    mlflow models build-docker -m "models:/zenml-prophet-model4/3" -n zenml-prophet-model4
    docker run -p 5333:8080 zenml-prophet-model4:3

   http://localhost:8501


    ```