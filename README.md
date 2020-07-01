# AWS-DevSecOps-Factory
Sample DevSecOps pipelines (heavily biased on the "Sec") for various stacks and tools using open-source security tools and AWS native services. Stop in, pick what you want, add your own!

[![DepShield Badge](https://depshield.sonatype.org/badges/jonrau1/AWS-DevSecOps-Factory/depshield.svg)](https://depshield.github.io)

## Table of Contents
TODO

## Description
The AWS-DevSecOps-Factory is a consolidation of a variety of work I had done to create DevSecOps pipelines using AWS native tools. In reality these are more like automated AppSec pipelines that you would bolt on to the start of your release train. That approach will be the least maintainence and ideally you would commit artifacts supported by the pipeline to be scanned before creating a release candidate from them. This repository will continually grow (hopefully through outside contributions) and is focused on using open-source security tools to deliver functionality. At times I will use commercial or "freemium" (commercial tools with a functional free tier). Being an AWS solutions library all security-related findings from the various tools will be parsed and written to Security Hub to tie your SecOps people and processes closer to your DevSecOps development groups.

## How to use this repository
Each available pipeline will have an architecture diagram with high-level steps / actions, at the bottom of the steps a link to the directory containing the code is provided as a hyperlink. You can deploy the solution with CloudFormation after uploading a ZIP archive to an S3 bucket, or, you can go into the `/src/` subdirectory of each solution to view the raw files (example artifacts, buildspec and Python scripts).

## Capability set (this will be subject to change)

### Security Tools
- **Secret detection**: [Detect-Secrets](https://github.com/Yelp/detect-secrets)
- **Linting**: [TFLint](https://github.com/terraform-linters/tflint), [cfn-python-lint](https://github.com/aws-cloudformation/cfn-python-lint), [Hadolint](https://github.com/hadolint/hadolint)
- **SAST**: [Bandit](https://github.com/PyCQA/bandit), [TFSec](https://github.com/liamg/tfsec), [Checkov](https://github.com/bridgecrewio/checkov), [Cfn-nag](https://github.com/stelligent/cfn_nag), [Cfripper](https://github.com/Skyscanner/cfripper), [Polaris](https://github.com/FairwindsOps/polaris), [sKan](https://github.com/alcideio/skan)
- **OSSec / License management**: [Snyk](https://github.com/snyk/snyk), [Whitesource](https://github.com/whitesource/agents)
- **Vulnerability management**: [Trivy](https://github.com/aquasecurity/trivy), [Dagda](https://github.com/eliasgranderubio/dagda)
- **Anti-virus / anti-malware**: [Dagda](https://github.com/eliasgranderubio/dagda), [ClamAV](https://www.clamav.net/documents/clam-antivirus-user-manual)

### Not security tools?
- **Source code management**: CodeCommit
- **Continuous integration**: CodeBuild
- **Continuous deployment**: CodePipeline
- **Secrets management**: Systems Manager Parameter Store

## Pipelines

### CloudFormation DevSecOps Pipeline
Architecture

[**Start Here**](/cloudformation-pipeline)

### Terraform DevSecOps Pipeline
Architecture

[**Start Here**](/terraform-pipeline)

### Docker image DevSecOps Pipeline (using Whitesource)
![Docker-DevSecOps-WSS](/docker-pipeline-wss/docker-pipeline-wss-architecture.jpg)
1. DevSecOps engineers use AWS Cloud9 as their Integrated Development Environment (IDE), here they can develop code, test locally, push commits, share access and benefit from security controls provided by VPCs and IAM
1. Upon commits to the master branch, CodePipeline automatically starts CI tests via different CodeBuild projects. We will use Hadolint, Detect-Secrets, Bandit, Snyk and Trivy to perform different security assessments that will be explained later
1. All logs from CodePipeline and CodeBuild are pushed to CloudWatch Logs (and optionally S3), to offload the need to continuously clone our source repository, artifacts are backed up to S3 where they are access controlled and encrypted
4. To promote code reuse and secure sensitive details like API keys and webhook tokens they will be injected into our build environment variables using AWS Systems Manager Parameter Store
5. All security assessments that fail will fail their build stage, which stops the pipeline, and findings from which will be sent to AWS Security Hub to be aggregated and have actions taken on them
6. After remediating various findings our Flash Docker image is pushed to Amazon Elastic Container Registry (ECR) where it can be used on a Fargate or EKS cluster

[**Start Here**](/docker-pipeline-wss)

### Docker image DevSecOps Pipeline (using Snyk)
![Docker-DevSecOps-WSS](/docker-pipeline-snyk/docker-pipeline-snyk-architecture.jpg)
1. DevSecOps engineers use AWS Cloud9 as their Integrated Development Environment (IDE), here they can develop code, test locally, push commits, share access and benefit from security controls provided by VPCs and IAM
1. Upon commits to the master branch, CodePipeline automatically starts CI tests via different CodeBuild projects. We will use Hadolint, Detect-Secrets, Bandit, Snyk and Trivy to perform different security assessments that will be explained later
1. All logs from CodePipeline and CodeBuild are pushed to CloudWatch Logs (and optionally S3), to offload the need to continuously clone our source repository, artifacts are backed up to S3 where they are access controlled and encrypted
4. To promote code reuse and secure sensitive details like API keys and webhook tokens they will be injected into our build environment variables using AWS Systems Manager Parameter Store
5. All security assessments that fail will fail their build stage, which stops the pipeline, and findings from which will be sent to AWS Security Hub to be aggregated and have actions taken on them
6. After remediating various findings our Flash Docker image is pushed to Amazon Elastic Container Registry (ECR) where it can be used on a Fargate or EKS cluster

[**Start Here**](/docker-pipeline-snyk)

### Kubernetes deployment Pipeline
Architecture

[**Start Here**](/k8s-pipeline)

### Docker + Kubernetes 2-stager Pipeline
Architecture

[**Start Here**](/docker-k8s-double-decker)