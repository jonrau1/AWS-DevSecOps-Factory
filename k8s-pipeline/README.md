# Kubernetes Security Scanning - CodeSuite 
Sample implementation of a Kubernetes security testing and deployment pipeline using the AWS CodeSuite. CodeCommit is used as the SCM, CodeBuild projects are used as the CI servers and CodePipeline is the CD automation engine which will start builds as new code is pushed (directly or via PR) to the Master branch. This pipeline assumes you have an *existing* EKS cluster that you have access to the IAM entity that created it with. This pipeline also uses an image from Docker Hub instead of from ECR.

If you do not have an EKS cluster or want a refresher refer to the [Getting started with eksctl](https://docs.aws.amazon.com/eks/latest/userguide/getting-started-eksctl.html) section of the Amazon EKS User Guide for a walkthrough on installing `kubectl`, `eksctl` and creating your first cluster. For information on installing `kubectl` on various OS flavors see [this page](https://kubernetes.io/docs/tasks/tools/install-kubectl/). 

This pipeline will look for regex and high-entropy based secrets/sensitive values using Detect-Secrets. Alcide's sKan and Fairwind's Polaris are used to perform static analysis on K8s deployments and Helm charts to look for security and best practice violations. The last build stage will authenticate and apply your `deployment.yaml` that was just scanned to your EKS Cluster.

## Solution architecture
![Architecture Diagram](./k8s-pipeline-architecture.jpg)

## Getting Started
1. Clone this repository and upload `k8s-devsecops.zip` to a bucket of your choosing. You can view the individual CodeBuild `buildspec`  
2. Deploy a stack from `k8s-secdevops.yml` in your AWS account, all necessary artifacts will be pushed as the first commit to the created CodeCommit repository. **Note** the first deployment will fail because your CodeBuild IAM Role does not have the required RBAC access into your cluster.
3. After the Stack has finished creating navigate to the Resources tab and copy the ARN of the IAM Role for CodeBuild, you may need to select the hyperlink to be taken to the IAM Console. After you have the ARN run the following command to generate an `aws-auth` ConfigMap:
```bash
aws eks --region $AWS_REGION update-kubeconfig --ame $AWS_CLUSTER_NAME
kubectl get configmaps aws-auth -n kube-system -o yaml > aws-auth.yaml
```
4. Open and edit the `aws-auth.yaml` file to add the CodeBuild role to `data.mapRoles` - replace the placeholder values with your Account Number and the name of the CodeBuild role:
```yaml
- rolearn: arn:aws:iam::$ACCOUNT_ID:role/$CODE_BUILD_ROLE_NAME
  username: $CODE_BUILD_ROLE_NAME
  groups:
    - system:masters
```
Your finalized `aws-auth.yaml` should somewhat resemble the following:
```yaml
apiVersion: v1
data:
  mapRoles: |
    - rolearn: arn:aws:iam::$ACCOUNT_ID:role/NodeInstanceRole
      username: system:node:{{EC2PrivateDNSName}}
      groups:
      - system:bootstrappers
      - system:nodes      
    - rolearn: arn:aws:iam::$ACCOUNT_ID:role/$CODE_BUILD_ROLE_NAME
      username: $CODE_BUILD_ROLE_NAME
      groups:
        - system:masters        
kind: ConfigMap
metadata:
  name: aws-auth
  namespace: kube-system
```
5. Set the new configuration on your cluster: `kubectl apply -f aws-auth.yaml`
6. Navigate to the AWS CodePipeline Console, select the K8s pipeline and choose **Release Change** on the top-right of the console. This will manually restart the entire pipeline form the last commit in your source

To utilize the scanning tools deployed in this solution, upload all K8s YAML configs or Helm charts into the `/artifacts` subdirectory in the solution. You will need to clone the CodeCommit repository or upload the files manually. Refer to the [Getting started](https://docs.aws.amazon.com/codecommit/latest/userguide/getting-started-topnode.html) section of the AWS CodeCommit User Guide for help with either.

If you use JSON to define your k8s Deployments, or if you use Helm charts, you will need to modify all example `*-buildspec.yaml` files in `src/buildspecs/` and push the entire thing again.