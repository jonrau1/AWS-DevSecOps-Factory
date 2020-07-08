# Golden Amazon Machine Image (AMI) Pipelines
Various implementations of Golden AMI Pipelines built by AWS EC2 Image Builder and deployed via CloudFormation. The implementation examples include Amazon Linux 2, Ubuntu 18.04LTS and Windows Server 2019. At a minimum, each Pipeline includes Recipe Components which install the latest security updates. AWS does not seem to have feature parity across all of the support OS flavors hence the gaps. For for information see the **Capability Set** section.

## Capability Set
- Amazon Linux 2 (`GoldenAMIPipeline_AMZL2_CFN.yaml`)
  - [DISA STIG](https://docs.aws.amazon.com/imagebuilder/latest/userguide/image-builder-stig.html#ie-os-stig) Low configuration. Low (Cat. III) includes "Any vulnerability that degrades measures to protect against loss of confidentiality, availability, or integrity." 
  - Install Python 3
  - Apply Linux security updates
  - Inspector CIS Benchmark test. Performs a Center for Internet Security (CIS) security assessment of an instance with AWS Inspector Service.
  - Reboot test: Tests whether the system can reboot successfully
- Ubuntu 18.04LTS (`GoldenAMIPipeline_Ubuntu18_CFN.yaml`)
  - Install Python 3, Pip3, AWSCLI and Kubectl (custom Component)
  - Install Inspector Agent (custom Component)
  - Apply Linux security updates
  - Reboot test: Tests whether the system can reboot successfully
- Windows Server 2019 (`GoldenAMIPipeline_WS19_CFN.yaml`)
  - [DISA STIG](https://docs.aws.amazon.com/imagebuilder/latest/userguide/image-builder-stig.html#ie-os-stig) Low configuration. Low (Cat. III) includes "Any vulnerability that degrades measures to protect against loss of confidentiality, availability, or integrity." 
  - Install PowerShell Core 6.2.4
  - Install Python 3
  - Inspector CIS Benchmark test. Performs a Center for Internet Security (CIS) security assessment of an instance with AWS Inspector Service.
  - Reboot test: Tests whether the system can reboot successfully

## Getting Started
**Note** Each CloudFormation template will create an EC2 Image Builder pipeline and all related services without sharing them between templates. This means you can have multiple IAM Roles, S3 Buckets and Instance Profiles that do the same thing but are just named differently.

1. Create a stack from any of the CloudFormation templates
2. After creation navigate to the EC2 Image Builder console, select the Pipeline and choose Run from the Actions dropdown