# Docker Security Scanning - CodeSuite 
Sample implementation of a Docker security testing pipeline using the AWS CodeSuite. CodeCommit is used as the SCM, CodeBuild projects are used as the CI servers and CodePipeline is the CD automation engine which will start builds as new code is pushed (directly or via PR) to the Master branch. Elastic Container Registry is used to store the finalized Docker image.

This pipeline lints Dockerfiles using Hadolint, looks for regex and high-entropy based secrets/sensitive values using Detect-Secrets and performs software composition analysis (dependency vulnerability test & lisc. inventory) using Whitesource. Dagda is used to perform anti-virus/anti-malware checks and additional vulnerabillity testing on the layers and dependencies is done using various Red Hat and NVD databases and open-source SAST tools such as GoSec and Bandit. Finally, Trivy is used to perform layer vulnerability analysis on most major parent images before the scanned image is pushed to ECR.

## Getting Started
Clone this repository and upload `docker-devsecops.zip` to a bucket of your choosing. You can view the individual CodeBuild `buildspec`'s in `src/buildspecs/`.

Create SSM Parameters for your Whitesource API Key and User Key (for your CI user) as these will be needed for parameters in the CloudFormation template. You will also need to know the name of your Product (i.e. Infosec-dev)
```bash
aws ssm put-parameter --name wssApiKey --type SecureString --value <API_KEY>
aws ssm put-parameter --name wssUserKeyParameter --type SecureString --value <USER_KEY>
```

Deploy a stack from `docker-secdevops.yml` in your AWS account, all necessary artifacts will be pushed as the first commit to the created CodeCommit repository.

To test your own Dockerfile and dependencies push those artifacts to the `/src/artifacts/` directory.

**Note:** Modify your Config file for WSS to tailor to your codebase.