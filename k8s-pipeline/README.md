# Kubernetes Security Scanning - CodeSuite 
Sample implementation of a Kubernetes security testing and deployment pipeline using the AWS CodeSuite. CodeCommit is used as the SCM, CodeBuild projects are used as the CI servers and CodePipeline is the CD automation engine which will start builds as new code is pushed (directly or via PR) to the Master branch. This pipeline assumes you have an *existing* EKS cluster that you have access to the IAM entity that created it with. This pipeline also uses an image from Docker Hub instead of from ECR.

This pipeline will look for regex and high-entropy based secrets/sensitive values using Detect-Secrets. Alcide's sKan and Fairwind's Polaris are used to perform static analysis on K8s deployments and Helm charts to look for security and best practice violations. The last build stage will authenticate and apply your `deployment.yaml` that was just scanned to your EKS Cluster.

## Before you start
**If you have an existing EKS cluster that you have `system:masters` RBAC access into you can skip this section**

**Note**: If you do not have an EKS cluster and would rather use `eksctl` to create it refer to the [Getting started with eksctl](https://docs.aws.amazon.com/eks/latest/userguide/getting-started-eksctl.html) section of the Amazon EKS User Guide. If you use `eksctl` or use the below methods, ensure it is with an IAM principal that you can get access to readily to add additional IAM principals to the Cluster RBAC. It is recommended that you take these actions from a Cloud9 IDE with an Instance Profile attached.

1. Install or upgrade your AWS CLI to the latest version. Ensure it is at least version `1.16.156`.
```bash
sudo apt install -y python3 python3-pip
pip3 install awscli
aws --version
```

2. [Install](https://kubernetes.io/docs/tasks/tools/install-kubectl/) `kubectl` on your system. Ensure it is at least version `1.16`.
```bash
curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
kubectl version --short --client
```

3. Create the EKS Cluster service role by navigating to the IAM Console, creating a Role and choosing **EKS - Cluster** from the list of service use cases. It will automatically attach the necessary service role permissions. Give your Role a unique name and create it.

4. If you do not have a VPC with public and private subnets you can use this [AWS-provided template](https://amazon-eks.s3.us-west-2.amazonaws.com/cloudformation/2020-06-10/amazon-eks-vpc-private-subnets.yaml). You should specify at least one Private and one Public subnet for the next step. You should also have a Security Group that *at least* allows access on HTTPS (TCP 443).

5. Create an EKS Cluster with the CLI. Replace the placeholder values with your Role Name, Subnet IDs and Security Groups. This can take up to 20 minutes to complete and will only provision the Cluster and *not* the Node Groups. If you wanted to specify other values refer to the create-cluster CLI command [here](https://docs.aws.amazon.com/cli/latest/reference/eks/create-cluster.html).
```bash
aws eks create-cluster \
    --kubernetes-version 1.16 \
    --name devsecops-demo \
    --role-arn $ROLE_NAME \
    --resources-vpc-config subnetIds=$SUBNET_1,$SUBNET_2,securityGroupIds=$SECURITY_GROUP
```

6. After your EKS Cluster has finished creating, authenticate to the cluster and interact with it using `kubectl` to ensure everything is working as expected.
```bash
aws eks --region $AWS_REGION update-kubeconfig --name devsecops-demo
kubectl get svc
```

7. Create an IAM role for Managed Node Groups, navigate to the IAM Console and create a role with the EC2 common use case. Attach the below AWS Managed Policies and finish creating the role. You should give a name such as **NodeInstanceRole-* and change the default description.
```bash
AmazonEKSWorkerNodePolicy
AmazonEKS_CNI_Policy
AmazonEC2ContainerRegistryReadOnly
```

8. Create a Managed Node Group with the CLI. Repalce the placeholder values as necessary. **Note** the subnets should be configured to automatically assign Public IPs otherwise the health check for the Node Groups will fail.
```bash
aws eks create-nodegroup \
    --cluster-name devsecops-demo \
    --nodegroup-name devsecops-node-group \
    --subnets $SUBNET_1 $SUBNET_2 \
    --instance-types t3.medium \
    --node-role $NODEGROUP_IAM_ROLE
```

9. After the Node Group has finished creating you can move onto the next steps. This is important because it will create an AWS authentication Config Map in the `kube-system` namespace that you will interact with in Step 4 of the next session.

## Getting Started
1. Clone this repository and upload `k8s-devsecops.zip` to a bucket of your choosing.
2. Deploy a CloudFormation Stack from `K8s_DevSecOps_Pipeline_CFN.yaml` in your AWS account, all necessary artifacts will be pushed as the first commit to the created CodeCommit repository. **Note** the first deployment will fail because your CodeBuild IAM Role does not have the required RBAC access into your EKS Cluster.
3. After the Stack has finished creating navigate to the Resources tab and copy the ARN of the IAM Role for CodeBuild, you may need to select the hyperlink to be taken to the IAM Console - you *may* be able to catch the IAM Role ARN before the Stack finishes creating. After you have the ARN run the following command to generate an `aws-auth` ConfigMap:
```bash
aws eks --region $AWS_REGION update-kubeconfig --ame $AWS_CLUSTER_NAME
kubectl get configmaps aws-auth -n kube-system -o yaml > aws-auth.yaml
```
4. Open and edit the `aws-auth.yaml` file to add the CodeBuild role to `data.mapRoles` - replace the placeholder values with your Account Number and the name of the CodeBuild role:
```yaml
- groups:
  - system:masters
  rolearn: arn:aws:iam::$ACCOUNT_NUMBER:role/K8sDevSecOps-CodeBuildServiceRole
  username: K8sDevSecOps-CodeBuildServiceRole
```
Your finalized `aws-auth.yaml` should somewhat resemble the following:
```yaml
apiVersion: v1
data:
  mapRoles: |
    - groups:
      - system:masters
      rolearn: arn:aws:iam::$ACCOUNT_NUMBER:role/K8sDevSecOps-CodeBuildServiceRole
      username: K8sDevSecOps-CodeBuildServiceRole
    - groups:
      - system:bootstrappers
      - system:nodes
      rolearn: arn:aws:iam::$ACCOUNT_NUMBER:role/NodeInstanceRole-DevSecOps
      username: system:node:{{EC2PrivateDNSName}}
kind: ConfigMap
metadata:
  creationTimestamp: ""
  name: aws-auth
  namespace: kube-system
```
5. Set the new configuration on your cluster: `kubectl apply -f aws-auth.yaml`
6. Navigate to the AWS CodePipeline Console, select the K8s pipeline and choose **Release Change** on the top-right of the console. This will manually restart the entire pipeline form the last commit in your source

To utilize the scanning tools deployed in this solution, upload all K8s YAML configs or Helm charts into the `/artifacts` subdirectory in the solution. You will need to clone the CodeCommit repository or upload the files manually. Refer to the [Getting started](https://docs.aws.amazon.com/codecommit/latest/userguide/getting-started-topnode.html) section of the AWS CodeCommit User Guide for help with either.

If you use JSON to define your k8s Deployments, or if you want to scan your Helm Charts, you will need to modify all example `*-buildspec.yaml` files in `src/buildspecs/` and push the entire solution again.