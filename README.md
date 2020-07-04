# AWS-DevSecOps-Factory
Sample DevSecOps pipelines (heavily biased on the "Sec") for various stacks and tools using open-source security tools and AWS native services. Stop in, pick what you want, add your own!

## Table of Contents
- Description
- How to use
- Capability set
- Pipelines
- FAQ

## Description
The AWS-DevSecOps-Factory is a consolidation of a variety of work I had done to create DevSecOps pipelines using AWS native tools. In reality these are more like automated AppSec pipelines that you would bolt on to the start of your release train. That approach will be the least maintainence and ideally you would commit artifacts supported by the pipeline to be scanned before creating a release candidate from them. This repository will continually grow (hopefully through outside contributions) and is focused on using open-source security tools to deliver functionality. At times I will use commercial or "freemium" (commercial tools with a functional free tier). Being an AWS solutions library all security-related findings from the various tools will be parsed and written to Security Hub to tie your SecOps people and processes closer to your DevSecOps development groups.

## How to use this repository
Each available pipeline will have an architecture diagram and a link to the directory containing the code is provided as a hyperlink. The subdirectories will have a more detailed walkthrough of steps, prerequisites and deployment considerations. You can deploy the solution with CloudFormation after uploading a ZIP archive to an S3 bucket, or, you can go into the `/src/` subdirectory of each solution to view the raw files (example artifacts, buildspec and Python scripts).

## Capability set (this will be subject to change)

### Security Tools
- **Secret detection**: [Detect-Secrets](https://github.com/Yelp/detect-secrets)
- **Linting**: [TFLint](https://github.com/terraform-linters/tflint), [cfn-python-lint](https://github.com/aws-cloudformation/cfn-python-lint), [Hadolint](https://github.com/hadolint/hadolint)
- **Platform SAST**: [TFSec](https://github.com/liamg/tfsec), [Checkov](https://github.com/bridgecrewio/checkov), [Cfn-nag](https://github.com/stelligent/cfn_nag), [Cfripper](https://github.com/Skyscanner/cfripper), [Polaris](https://github.com/FairwindsOps/polaris), [sKan](https://github.com/alcideio/skan)
- **Code-specific SAST**: [Bandit](https://github.com/PyCQA/bandit), [Gosec](https://github.com/securego/gosec)
- **OSSec / License management**: [Snyk](https://github.com/snyk/snyk), [Whitesource](https://github.com/whitesource/agents), [OWASP DependencyCheck](https://github.com/jeremylong/DependencyCheck) (via Dagda)
- **Vulnerability management**: [Trivy](https://github.com/aquasecurity/trivy), [Dagda](https://github.com/eliasgranderubio/dagda)
- **Anti-virus / anti-malware**: [Dagda](https://github.com/eliasgranderubio/dagda), [ClamAV](https://www.clamav.net/documents/clam-antivirus-user-manual)

### Developement Tools
- **Source code management**: AWS CodeCommit
- **Continuous integration**: AWS CodeBuild
- **Continuous deployment**: AWS CodePipeline
- **Secrets management**: AWS Systems Manager Parameter Store
- **Artifact management**: AWS S3 (you can also use AWS CodeRepository)

## Pipelines

### CloudFormation DevSecOps Pipeline
![CloudFormation DevSecOps Architecture](/cloudformation-pipeline/cloudformation-pipeline-architecture.jpg)

[**Start Here**](/cloudformation-pipeline)

### Terraform DevSecOps Pipeline
![Terraform DevSecOps Architecture](/terraform-pipeline/terraform-pipeline-architecture.jpg)

[**Start Here**](/terraform-pipeline)

### Docker image DevSecOps Pipeline (using Whitesource)
![Docker-DevSecOps-WSS](/docker-pipeline-wss/docker-pipeline-wss-architecture.jpg)

[**Start Here**](/docker-pipeline-wss)

### Docker image DevSecOps Pipeline (using Snyk)
![Docker-DevSecOps-WSS](/docker-pipeline-snyk/docker-pipeline-snyk-architecture.jpg)

[**Start Here**](/docker-pipeline-snyk)

### Kubernetes deployment DevSecOps Pipeline
![Kubernetes DevSecOps Architecture](/k8s-pipeline/k8s-pipeline-architecure.jpg)

[**Start Here**](/k8s-pipeline)

### Docker + Kubernetes 2-stager DevSecOps Pipeline
![Docker-K8s-Architecture](/docker-k8s-double-decker/docker-k8s-double-decker-architecture.jpg)

[**Start Here**](/docker-k8s-double-decker)

### Flask DevSecOps Pipeline
![Flask DevSecOps Architecture](/flask-pipeline/flask-pipeline-architecture.jpg)

[**Start Here**](/flask-pipeline)

### Go application DevSecOps Pipeline
Architecture TODO

[**Start Here**](/golang-pipeline)

## FAQ

### 1. What is DevSecOps? How different is it than DevOps?

### 2. What leads to success in DevSecOps?

### 3. What are guiding principles or concepts about DevSecOps?

### 4. If an organization already has a DevOps culture or delivers software in a DevOps-y pattern, how do they make the lead into DevSecOps?

### 5. What does DevSecOps done wrong look like? Are there anti-patterns to look for or pitfalls to avoid?
 
### 6. I "do" DevSecOps! Can I get rid of my AppSec or Vulnerability Management program now...?

### 7. Where do I go from here?

### 8. If I am fostering a DevSecOps culture on AWS does that mean I need to use AWS tools?

### 9. What other elements or codes of practice should I incorporate in my DevSecOps program that aren't necessarily called out?