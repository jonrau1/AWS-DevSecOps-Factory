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
- **Secret detection**: Detect-Secrets
- **Linting**: TFLint, Python-CFN-Lint, Hadolint
- **SAST**: Bandit, TFSec, Checkov, Cfn-nag, Cfripper, Polaris, sKan
- **OSSec / License management**: Snyk, Whitesource
- **Vulnerability management**: Trivy, Dagda
- **Anti-virus / anti-malware**: Dagda, ClamAV

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
Architecture

[**Start Here**](/docker-pipeline-wss)

### Docker image DevSecOps Pipeline (using Snyk)
Architecture

[**Start Here**](/docker-pipeline-snyk)

### Kubernetes deployment Pipeline
Architecture

[**Start Here**](/k8s-pipeline)

### Docker + Kubernetes 2-stager Pipeline
Architecture

[**Start Here**](/docker-k8s-double-decker)