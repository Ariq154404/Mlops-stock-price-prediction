commands
 ```bash
    minikube start driver=docker
    python3.9 -m venv myenv
    source myenv/bin/activate
    cd data-engineering
    cd manifests
    kubectl apply -f mysql-deployment.yaml
    kubectl apply -f kafka-deployment.yaml
    kubectl get pods
    kubectl get svc
    kubectl apply -f mysql-service.yaml
    kubectl apply -f kafka-service.yaml
    docker build -t ariq913/stock_mysql_creation:latest .
    docker push ariq913/stock_mysql_creation:latest
    kubectl delete service mysql-service
    kubectl apply -f create-db.yaml
kubectl delete service kafka-service
    ```