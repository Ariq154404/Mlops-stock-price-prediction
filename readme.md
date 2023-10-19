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
    docker run -p 5000:5000 prophet_forecaster

   http://localhost:8501


    ```