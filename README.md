# Cloud Task Manager: Docker + Kubernetes

A small Flask task manager for demonstrating application containerization and Kubernetes deployment.

## Features
- Add, complete, and delete tasks
- `/health` endpoint for Kubernetes health probes
- `/api/tasks` JSON endpoint
- Docker image and container
- Kubernetes Deployment with two replicas
- Kubernetes NodePort Service
- Container runs as a non-root user

> Note: Tasks are held in application memory for this assignment demo. They reset when a container restarts, and separate replicas do not share task data. For persistent, consistent data, add a database and persistent storage.

## Requirements
Install Docker Desktop, `kubectl`, and Minikube. Keep Docker Desktop running. Official Minikube setup: https://minikube.sigs.k8s.io/docs/start/

## 1. Run directly with Python (optional)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```
Open http://localhost:5000.

## 2. Build and run with Docker
Run these commands from the project root:
```powershell
docker build -t task-manager:1.0 .
docker run --rm -p 5000:5000 task-manager:1.0
```
Open http://localhost:5000. In another terminal, test:
```powershell
Invoke-RestMethod http://localhost:5000/health
Invoke-RestMethod http://localhost:5000/api/tasks
```
Stop the container with Ctrl+C in its terminal.

## 3. Start Kubernetes
```powershell
minikube start --driver=docker
kubectl get nodes
```

## 4. Make the local image available to Minikube
Build directly into Minikube's image store:
```powershell
minikube image build -t task-manager:1.0 .
minikube image ls
```
This avoids pushing the image to a public registry for a local demo.

## 5. Deploy
```powershell
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl rollout status deployment/task-manager
kubectl get deployments
kubectl get pods -o wide
kubectl get services
```
Wait until both pods show `Running` and `READY 1/1`.

## 6. Open the application
```powershell
minikube service task-manager-service
```
Minikube should open the service URL. If you need a stable local URL, use a second terminal:
```powershell
kubectl port-forward service/task-manager-service 8080:80
```
Then open http://localhost:8080.

## 7. Demonstrate scaling and self-healing
Scale from two to three replicas:
```powershell
kubectl scale deployment task-manager --replicas=3
kubectl get pods
```
Return to two replicas:
```powershell
kubectl scale deployment task-manager --replicas=2
```
To demonstrate self-healing, delete one pod by its actual name:
```powershell
kubectl get pods
kubectl delete pod <actual-pod-name>
kubectl get pods -w
```
Explain that the Deployment controller creates a replacement pod. Press Ctrl+C to stop watching.

## 8. Collect execution evidence
Capture your own screenshots showing:
1. `docker build` completing successfully.
2. `docker images` showing `task-manager:1.0`.
3. The app open in a browser.
4. `docker ps` showing the running container.
5. `kubectl get deployments,pods,services`.
6. The application open through the Kubernetes Service.
7. Scaling to three pods and the replacement pod after deletion.
8. `/health` returning a healthy response.

Do not use fabricated screenshots. Capture the commands and results from your own machine.

## 9. Cleanup
```powershell
kubectl delete -f k8s/service.yaml
kubectl delete -f k8s/deployment.yaml
minikube stop
```

## Suggested 3–5 minute recording
1. Introduce the app and architecture.
2. Explain the Dockerfile, then build and run the image.
3. Show the browser and health endpoint.
4. Explain the Deployment, replicas, probes, labels/selectors, and Service.
5. Apply the YAML and show the pods and Service.
6. Open the Kubernetes-hosted app.
7. Demonstrate scaling and self-healing.
8. Summarize containers vs. pods, Deployment vs. Service, and local vs. cloud deployment.

## Architecture
Browser → Kubernetes NodePort Service → one of the Task Manager Pods → Flask application

The Deployment maintains two pod replicas. The Service selects pods by the `app: task-manager` label and routes traffic to port 5000.
