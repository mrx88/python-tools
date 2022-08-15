# Introduction

Simple program to download all video files from a defined YouTube channel. Files will be downloaded to the defined directory and into sub-directories sorted by date.

## Usage

```bash
python main.py --help

Usage: main.py [OPTIONS]

  Main function

Options:
  --url TEXT               YouTube channel URL  [required]
  --resolution [low|high]  Video resolution
  --vid_dir TEXT           Video <directory> location
  --last INTEGER           Number of last videos to download
  --help                   Show this message and exit.
```

## Examples

### Download all videos

```bash
python main.py --url https://www.youtube.com/channel/UC57acx8sCmE7uFHfVMvIlNg --resolution high --vid_dir Videos/        
New daily videos in Videos/2022-07-10: ['Devops Tutorials  How to do Port Forwarding in Kubernetes Pods and How it  Works  Kubernetes.mp4']
New daily videos in Videos/2022-07-27: ['DevOps Tutorials  How to Assign CPU Resources to a Container Pods  Kubernetes Tutorials.mp4']
New daily videos in Videos/2022-07-07: ['DevOps Tutorials  How to Configure and Assign CPU and RAM Resources to Kubernetes Pods.mp4']
New daily videos in Videos/2022-07-03: ['DevOps Tutorials  How to attach a volume to kubernetes pod  Kubernetes Volumes explained.mp4']
New daily videos in Videos/2022-07-05: ['DevOps Tutorials  How to Deploy Deployments and Services in Kubernetes and Expose  Kubernetes.mp4']
New daily videos in Videos/2022-07-24: ['DevOps Tutorials  How to Secure Kubernetes Services with Ingress and Lets Encrypt  Kubernetes.mp4']
New daily videos in Videos/2022-06-21: ['AWS Tutorials  How to Manage an EC2 Instances  start and stop  via AWS CLI (Command Line Interface.mp4']
New daily videos in Videos/2022-06-20: ['AWS Tutorials  How to Create and Manage an AWS S3 Bucket Using Terraform  Terraform Tutorials.mp4']
New daily videos in Videos/2022-06-28: ['DevOps Tutorials  How to Run Ansible playbook Using Ansible Tags Attribute  Automation.mp4']
New daily videos in Videos/2022-07-26: ['DevOps Tutorials  How to deploy Kubernetes Dashboard quickly and easily And Monitor Resources.mp4']
New daily videos in Videos/2022-06-16: ['Kubernetes  how to install Kubernetes in your VMsInstances and  interact with the  K8s cluster.mp4', 'DevOps Tutorials  How to Setup and Enable Minikube Dashboard and metrics of Pods and Namespaces.mp4']
New daily videos in Videos/2022-07-18: ['DevOps Tutorials  Creating and Deploying multi-container pods in Kubernetes  Kubernetes.mp4']
...
```


### Download last X videos
```bash
python main.py --url https://www.youtube.com/channel/UC57acx8sCmE7uFHfVMvIlNg --resolution high --vid_dir Videos/ --last 3

New daily videos in Videos/2022-08-11: ['Kubernetes Tutorials  Configuring and Managing Kubernetes Persistent Storage Volumes  Kubernetes.mp4']
New daily videos in Videos/2022-08-09: ['Kubernetes Tutorials  Kubectl Basic Commands For Beginners  Kubernetes Commands.mp4']
New daily videos in Videos/2022-08-01: ['DevOps Tutorials  How to Setup Kubernetes Ingress load balancers using NGINX and TLS  Kubernetes.mp4']
Completed download of last 3 videos
```

## Logs

Log file is written to main.log in the same directory as the project.

## Development

```bash
export PIPENV_NO_INHERIT=true
pipenv --python 3.10.0
pipenv install
pipenv install --dev
```