commands
 ```bash
    minikube start driver=docker
    python3.9 -m venv myenv
    source myenv/bin/activate
    cd data-engineering
    cd manifests
    docker exec -it data-engineering_mysql_1 mysql -uroot -pmy-secret-pw
   kubectl apply -f rabbitmq-deployment.yaml
kubectl apply -f rabbitmq-service.yaml
kubectl apply -f mysql-deployment.yaml
kubectl apply -f mysql-service.yaml

    ```