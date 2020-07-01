# CloudFormation Security Scanning - CodeSuite 
Sample implementation of a CloudFormation security testing pipeline using the AWS CodeSuite. CodeCommit is used as the SCM, CodeBuild projects are used as the CI servers and CodePipeline is the CD automation engine which will start builds as new code is pushed (directly or via PR) to the Master branch. The final build stage also creates stacks from the template and separate parameter files.

This pipeline lints CloudFormation templates by using `python-cfn-lint` and looks for regex and high-entropy based secrets/sensitive values using Detect-Secrets. Various security static analysis is performed against the templates using CFRipper, Cfn-nag and Checkov, respectively. The final stage (Checkov) will also use the AWS CLI to create and deploy the stack(s).

## Before you start
All CloudFormation templates will need to be placed in the `/templates` directory regardless of their language. This is done to seperate them from external `parameters.json` files which will fail builds due to a syntax errors from reading these. This is also done to future-proof the solution in case you use JSON as your CloudFormation template language. **If you do use JSON** you will need to go through the `buildspec` files and change some of the tool commands to scan JSON templates as this is setup for YAML only right now.

It is reccomended that you create your own ZIP archive of your own templates, parameter files and modified CodeBuild `buildspec` and any other helper scripts. You will need to make an archive with `/templates`, `/params` and `/buildspecs` at the root **do not** send the whole `/src` directory to a ZIP archive.

## Getting Started
Clone this repository and upload `cfn-devsecops.zip` to a bucket of your choosing. Deploy a stack from `cfn-security-pipeline.yml` in your AWS account, all necessary artifacts will be pushed as the first commit to the created CodeCommit repository. 

**Important Note:** Modify the permissions of the CodeBuild Role in `cfn-security-pipeline.yml` to give it permissions for whatever you will be deploying from your deployment stack. I.e. if you will be deploying EKS clusters or ECS Services you should modify your permissions to include `eks` or `ecs-task` permissions.