# Kubernetes Security Scanning - CodeSuite 
Sample implementation of a Docker security testing pipeline using the AWS CodeSuite. CodeCommit is used as the SCM, CodeBuild projects are used as the CI servers and CodePipeline is the CD automation engine which will start builds as new code is pushed (directly or via PR) to the Master branch. Elastic Container Registry is used to store the finalized Docker image. 

This pipeline will look for regex and high-entropy based secrets/sensitive values using Detect-Secrets. Alcide's sKan and Fairwind's Polaris are used to perform static analysis on K8s deployments and Helm charts to look for security and best practice violations.

## Getting Started
Clone this repository and upload `k8s-devsecops.zip` to a bucket of your choosing. You can view the individual CodeBuild `buildspec` in `src/buildspecs/`. Deploy a stack from `k8s-secdevops.yml` in your AWS account, all necessary artifacts will be pushed as the first commit to the created CodeCommit repository.

The utilize the scanning utilities deployed in this solution, upload all K8s YAML configs or Helm charts into the `/artifacts` subdirectory in the solution.

If you use JSON to define your k8s Deployments, or if you use Helm charts, you will need to modify all example `*-buildspec.yaml` files in the solution.