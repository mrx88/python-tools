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

## Docker

```
docker build --pull --rm -f "Dockerfile" -t youtubevideos:latest "."
docker run youtubevideos --help 
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
New video added: Videos/2022-09-12/DevOps Tutorials  What is Terraform  Terraform basics for AWS Beginners  Terraform installation.mp4
New video added: Videos/2022-08-28/DevOps Tutorials  Creating K8s Nginx deployment and Expose a service Node port  cloudlearnhub.mp4
New video added: Videos/2022-09-06/DevOps Tutorials  Kubernetes cluster backup and restore with  Velero - Kubernetes cluster backup.mp4
New video added: Videos/2022-09-19/DevOps Tutorials  How to use Terraform Modules to build a AWS network VPC  Terraform Modules.mp4
New video added: Videos/2022-08-23/DevOps Tutorials  How to Create AWS VPC and Subnets Using Terraform  AWS Tutorials  Cloudlearnhub.mp4
New video added: Videos/2022-08-25/DevOps Tutorial  Setup Automated EC2 EBS Backups on AWS Using Terraform with Lambda and Cloud watch.mp4
...
```


### Download last X videos
```bash
python main.py --url https://www.youtube.com/channel/UC57acx8sCmE7uFHfVMvIlNg --resolution high --vid_dir Videos/ --last 3

New video added: Videos/2022-09-20/DevOps Tutorials  How to Deploy VM and VPC in Google Cloud Platform via Terraform  Terraform.mp4
New video added: Videos/2022-09-21/DevOps Tutorial  Understand Kubernetes Cluster Architecture  How to setup EKS Cluster on AWS.mp4
New video added: Videos/2022-09-25/DevOps Tutorials  Install Configuration & Validation Install Kubernetes Masters and Nodes on AWS.mp4
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