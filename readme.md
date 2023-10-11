commands
 ```bash
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
    docker build -t mlops-stock/mysql_creation:latest
    docker push mlops-stock/mysql_creation:latest
    kubectl delete service mysql-service
kubectl delete service kafka-service
    ```