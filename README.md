# Insider Python Selenium

This project is focused on creating a **Kubernetes infrastructure on AWS** and running **Selenium Python tests** in that environment. The goal is to automate the process of managing the testing environment using **EKS (Elastic Kubernetes Service)**, **Docker**, and **Selenium** to run automated Chrome browser tests.

## Prerequisites

- **Ubuntu 24.04** EC2 instance on AWS
- AWS account
- Python (for running Selenium tests)
- Docker installed
- Basic knowledge of Kubernetes and AWS services

## Project Setup

### Step 1: Install kubectl

Run the following commands to install `kubectl`:

```bash
curl -LO "https://dl.k8s.io/release/$(curl -Ls https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
kubectl version --client
```

### Step 2: Install AWS CLI

Run the following commands to install AWS CLI:
```bash
curl -s "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
aws --version
```

Configure AWS CLI:
```bash
aws configure
```
Enter the following details:

- AWS Access Key
- AWS Secret Key
- Region (e.g., us-west-1 for California)
- Output format (choose either json or yaml)


### Step 3: Install eksctl (EKS Management Tool)

Run the following commands to install eksctl, which is a simple command-line utility for creating and managing EKS clusters:
```bash
curl -sLO "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_Linux_amd64.tar.gz"
tar -xzf eksctl_Linux_amd64.tar.gz
sudo mv eksctl /usr/local/bin/
eksctl version
```

### Step 4: Install aws-iam-authenticator

Run the following commands to install the aws-iam-authenticator:
```bash
curl -LO "https://github.com/kubernetes-sigs/aws-iam-authenticator/releases/download/v0.6.30/aws-iam-authenticator_0.6.30_linux_amd64"
chmod +x aws-iam-authenticator_0.6.30_linux_amd64
sudo mv aws-iam-authenticator_0.6.30_linux_amd64 /usr/local/bin/aws-iam-authenticator
aws-iam-authenticator version
```

### Step 5: Create an EKS Cluster

Create an EKS cluster using the following eksctl command:
```bash
eksctl create cluster --name InsiderTestPython --region us-west-1 --nodegroup-name selenium-nodes --node-type t3.medium --nodes 2
```
This command will create an EKS cluster named InsiderTestPython in the us-west-1 region with a node group called selenium-nodes, which contains two t3.medium nodes.


### Step 6: Configure kubectl to Manage EKS Cluster

Once the cluster is created, configure kubectl to manage your newly created EKS cluster:
```bash
aws eks --region us-west-1 update-kubeconfig --name InsiderTestPython
```

## Docker Installation

### Install Docker on Ubuntu 24.04

Run the following commands to install Docker:
```bash
sudo apt update
sudo apt install -y docker.io
```

### Start and Enable Docker

Start and enable Docker to run at boot:

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

### Verify Docker Installation

Ensure that Docker was installed correctly by checking its version:
```bash
docker --version
```

## Create Elastic Container Registry (ECR)

### Step 1: Create an ECR Repository

To store Docker images in AWS, create an ECR repository:

```bash
aws ecr create-repository --repository-name insider-test-python --region us-west-1
```
Take note of the repository URI (e.g., XXXXXXXXX.dkr.ecr.us-west-1.amazonaws.com/insider-test-python).

### Step 2: Authenticate Docker with ECR

Authenticate your Docker client to interact with the ECR repository:

```bash
aws ecr get-login-password --region us-west-1 | docker login --username AWS --password-stdin XXXXXXXXX.dkr.ecr.us-west-1.amazonaws.com
```
Replace XXXXXXXXX with your AWS account ID.


