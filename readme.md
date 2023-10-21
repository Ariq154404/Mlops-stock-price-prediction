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
    zenml experiment-tracker register mlflow_tracker --flavor=mlflow
    zenml model-deployer register mlflow --flavor=mlflow
    zenml stack register mlflow_stack -a default -o default -d mlflow -e mlflow_tracker --set
    zenml stack update quickstart -r mlflow

   http://localhost:8501


    ```