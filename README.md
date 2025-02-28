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


### Step 2: Install AWS CLI

Run the following commands to install AWS CLI:
```bash
curl -s "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
aws --version
