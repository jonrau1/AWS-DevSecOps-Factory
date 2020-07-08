# AWS-DevSecOps-Factory
Sample DevSecOps pipelines (heavily biased on the "Sec") for various stacks and tools using open-source security tools and AWS native services. Stop in, pick what you want, add your own!

## Table of Contents
- [Description](https://github.com/jonrau1/AWS-DevSecOps-Factory#description)
- [How to use](https://github.com/jonrau1/AWS-DevSecOps-Factory#how-to-use-this-repository)
- [Capability set](https://github.com/jonrau1/AWS-DevSecOps-Factory#capability-set-this-will-be-subject-to-change)
- [Pipelines](https://github.com/jonrau1/AWS-DevSecOps-Factory#pipelines)
- [FAQ](https://github.com/jonrau1/AWS-DevSecOps-Factory#faq)

## Description
The AWS-DevSecOps-Factory is a consolidation of a variety of work I had done to create DevSecOps pipelines using AWS native tools. In reality these are more like automated AppSec pipelines that you would bolt on to the start of your release train. That approach will be the least maintainence and ideally you would commit artifacts supported by the pipeline to be scanned before creating a release candidate from them. This repository will continually grow (hopefully through outside contributions) and is focused on using open-source security tools to deliver functionality. At times I will use commercial or "freemium" (commercial tools with a functional free tier). Being an AWS solutions library all security-related findings from the various tools will be parsed and written to Security Hub to tie your SecOps people and processes closer to your DevSecOps development groups.

Given that this repository is heavily biased on security it is very worthwhile the [give this whitepaper a read](https://d0.awsstatic.com/whitepapers/DevOps/practicing-continuous-integration-continuous-delivery-on-AWS.pdf) for a broader picture into tradtional "DevOps" (see, actual testing)/

## How to use this repository
Each available pipeline will have an architecture diagram and a link to the directory containing the code is provided as a hyperlink. The subdirectories will have a more detailed walkthrough of steps, prerequisites and deployment considerations. You can deploy the solution with CloudFormation after uploading a ZIP archive to an S3 bucket, or, you can go into the `/src/` subdirectory of each solution to view the raw files (example artifacts, `buildspec`, `appspec` and Python scripts).

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
- **Infrastructure-as-Code**: [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)
- **Source code management**: [AWS CodeCommit](https://docs.aws.amazon.com/codecommit/latest/userguide/welcome.html)
- **Continuous integration**: [AWS CodeBuild](https://docs.aws.amazon.com/codebuild/latest/userguide/welcome.html)
- **Continuous delivery**: [AWS CodePipeline](https://docs.aws.amazon.com/codepipeline/latest/userguide/welcome.html), [AWS EC2 Image Builder](https://aws.amazon.com/image-builder/)
- **Continuous deployment**: [AWS CodeDeploy](https://d0.awsstatic.com/whitepapers/DevOps/practicing-continuous-integration-continuous-delivery-on-AWS.pdf)
- **Secrets management**: [AWS Systems Manager Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html)
- **Artifact management**: [AWS S3](https://docs.aws.amazon.com/AmazonS3/latest/gsg/GetStartedWithS3.html) (artifacts in this perspective refer to code that is shared between your CodePipeline stages)

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

### Golden AMI Pipeline
Architecture TODO

[**Start Here**](/golden-ami-pipeline)

## FAQ

### 1. What is DevSecOps? How different is it than DevOps?
Simply DevSecOps stands for “development, security and operations”, from the standpoint of principles and a high-level technology stack (e.g. automation, continuous integration / continuous delivery (CI/CD)) DevSecOps is not much different than DevOps. The goal of this ideology is to make security a shared responsibility in development and operations teams and carry over all the cultural benefits that DevOps seeks to boil up to the top such as agility, innovation, and speed. DevSecOps is synonymous in this aspect with “shifting security left” and that statement can be taken literally: automation and CI/CD sees the addition of security-focused tools where the main benefit is you may reduce or totally eliminate any misconfigurations or vulnerabilities from your software by the time it reaches production.

DevSecOps seeks to address the security gaps that a DevOps culture introduced due either to the inexperience and relative immaturity of the security organization, the DevOps organization, or both. An inexperienced security organization may have hampered velocity due to the introduction of manual stage gates just as threat modeling or long lead times of a traditional application security (AppSec) organization. An immature DevOps organization may have completely sacrificed any security testing in the name of speed only to introduce more vulnerabilities or misconfigurations had they taken the time to do it.

### 2. What leads to success in DevSecOps?
DevSecOps, like DevOps, is a cultural change and will require adherence to a core set of people, process, and technologies. Before starting your journey, you should consider what your software looks today and what it may look like 3, 6 or 12 months down the road. If available, you should also record your current technical debt and any vulnerabilities or other deficiencies surfaced by your AppSec, vulnerability management and/or cloud security posture management programs. These considerations must be taken into effect as it will define where you will concentrate your work before or during your shift to DevSecOps. For instance, if you have a lot of vulnerabilities due to a high amount of technical debt and your product roadmap is dictating a move to the cloud due to ROI or the perceived competitiveness it may bring to bear, you should take all of that into account.

Taking that previous example further, you should identify if you will be refactoring completely or upgrading to the latest versions and re-hosting / re-platforming, that will dictate what people need to be hired and what tools need to be purchased and/or built. If you will be undergoing the DevSecOps shift just for the sake of doing it or without the added complexities or refactoring or reducing technical debt you should benchmark your current posture and vulnerabilities to measure success against. Like DevOps, DevSecOps is also key performance indicator (KPI) driven and those should be created before investing the time in starting. Just adding some tools like Bandit or Black Duck into a toolchain is not “doing DevSecOps” – there must be measurement and accountability.

Needless to say you need to “pick the right tool for the right job” – if you are moving from on-premise to a cloud service provider you should invest in learning about cloud-native (e.g. Azure DevOps or AWS CodeBuild) solutions and also picking security and testing tools that align with your platform. Are you refactoring to .NET Core? You should find tools that support static analyst against .NET Core projects. With that in mind are you using packages that ***must*** run on Windows? If not, consider learning how to package and deploy software onto Linux using the `dotnet` CLI or `msbuild` - this OS shift can possibly bring ROI over Windows-based deployments

Lastly you should agree into delivery lifecycle apparatus that will coincide with your DevSecOps journey. If you are traditionally delivering software in quarterly slow iterations that may not be the right approach to achieve agility – you should consider training your product or project managers into an agile methodology such as Scrum or Kanban. Will you take any technical debt with you? What is your risk appetite – is not breaking builds on Medium CVE’s in line with your security program? Will you build in time to focus solely on remediation of vulnerabilities? All these things and more need to be weighed before starting and continually adjusted throughout your journey.

### 3. What are guiding principles or concepts about DevSecOps?
As touched on in #2 you should choose first to define some KPIs as well as key risk indicators (KRIs) to set a baseline when you start your DevSecOps journeys. These KPIs and KRIs should be allowed to adjust overtime as there are many variables that can bring you above or below those bars. Sometimes those KPIs and KRIs can be matched together, such as measuring that you are using the latest patches or major releases while also tracking if that move introduces new vulnerabilities to 0-days. Your KRIs can either be to measure operational risk, cyber risk or both and that should be lockstep with how your security program looks at risk, the appetite of risk and the acceptance (if any) of risk to and for the business.

Next, you should define a set of principles or tenets you are trying to achieve during your journey. These can be placed onto a Wiki or a Confluence page for your DevSecOps engineers and maybe your larger product ecosystem (or your whole company, preferably). Transparency is a large part of cultural success and setting public tenets or principles is a small piece of that. These can be very high-level such as committing to the minimum necessary usage of packages, the least privilege of all IAM roles / agreeing to never use an AWS managed policy or the strict guidance that there are to never be secrets in code. Ideally these principles, like your KPIs/KRIs, can be adjusted overtime but are forward looking (and maybe aspirational). Do you hardcode credentials in your `boto3` clients? Then it may make sense to boldly declare the elimination of secrets and refactoring of your code to support that.

The last concept that should be tackled is your security toolchain which are typically AppSec or vulnerability management type tools. There should be some tools that are non-negotiable and tools that are workload dependent. Just like in DevOps where you would have multiple pipelines to create different pieces of your software it is no different in DevSecOps. At a minimum you should seek to implement open-source or commercial statis analysis (aka SCA or SAST) tools to find deficiencies or vulnerabilities in your source code and dependencies. You should also consider the usage or linters and utilities to find secrets in your code base, these will help avoid breaking builds due to simple syntactic errors and committing hardcode credentials into your final product, respectively. Other platform-specific tooling or container security tools are more “boutique” and should only be used if you will use the platforms or intend to.

### 4. What does DevSecOps done wrong look like? Are there anti-patterns to look for or pitfalls to avoid?
DevSecOps (or even plain DevOps) done wrong is declaring that you “do it” without the necessary cultural commitment. Just using a SAST or vulnerability management tool in your pipeline is not DevSecOps, that is more like DevOps with a side of AppSec. DevSecOps is about the saturation of security principles and tools into your development cycles and taking ownership for any vulnerabilities found. Funneling deficiencies into a central organization for remediation (either your AppSec or Technical Operations (TechOps) organizations) is not DevSecOps. This journey comes knowing that your team is responsible for everything, including security, and its sacrifice or just running the tests and not acting on them is not good enough.

The first anti-pattern is the usage of tools for the sake of usage. Running security tools and override the failure exit codes or suppressing all checks is not conducive to a successful DevSecOps journey. The only time a finding should be suppressed or ignored if it is verified that it is a true false positive or a massive performance hit. The latter requires a formal risk acceptance, this is better handled by an enterprise or information risk management group (ERM/IRM) but you should include it as a logged item to revisit.

Another anti-pattern is running through redundant tools just to pad the usage of security tools. While there is value that can be found from using overlapping SAST tools or supplementing a commercial tool with a similar open-source one, just stacking security tests into your pipeline should be avoided. This can lead to longer build times or the surfacing of false positives or false negatives, you should always examine your tools for a fit and supplement or remove only when there is overwhelming evidence that it will lead to efficiencies.

A final example anti-pattern is not committing fully to a transparent culture. While some dislike the “name and shame” mantra that has become associated with gamification or publicizing results, this is an invaluable tool to drive accountability (and even some friendly competition) among teams. This does not always need to be from a centralized organization view, if you have the skills to create dashboards or automated narratives in your own team, you should do it. Dashboarding and transparency lets you and everyone else on your team / organization see if you are abiding by your KPIs/KRIs, tenets and principles. This does not need to be a negative – it is perfectly okay to re-base on real world performance. DevSecOps is called a journey for a reason, there are no dogmas within, every team will have a different experience and should remain flexible without sacrificing accountability in the adjustment of the supporting apparatus.
 
### 5. What other elements or codes of practice should I incorporate in my DevSecOps program that aren't necessarily called out?
(Warning, this is heavily opinionated). While not widely talked about, you should consider branching your DevSecOps journey out more broadly to your “traditional” centralized IT organization and other parts of the security organization – especially threat intelligence, IRM/ERM and legal. Your centralized IT organization may be responsible for things such as OS builds, maintaining Active Directory or general networking operations (hello Direct Connect and Transit Gateway). Those organizations should either be encouraged to adopt their own DevSecOps journey / methodology or co-opted directly or in part by your current one. Doing this helps solve two things – the outside dependency the “Ops” folks in your DevSecOps teams may run into (adding a route, opening a firewall rule, updating an IDS signature) and the inclusivity that comes with a positive DevSecOps culture. It is more likely your network operations team does not have the tools or training to be as agile as you are and not that they hate your guts. Getting these folks into ceremonies or otherwise included can be greatly beneficial for those reasons.

As far as the security and legal organizations go there are multiple reasons why you may want to include them. Your threat intelligence group can let you know if there are threat actors or other activity groups with the motivation and capability to target your product, you can use this to implement new tests, adopt a host-based security tool or even accelerate your refactoring to move your application out of the means of the attackers. You can also ask them for indicators of compromise (IOCs) such as hashes, IP addresses or domains to add to your existing perimeter protection tools and to have the “Ops” part of your team monitor for.

Talking with your ERM/IRM teams can help keep your KRIs in alignment, proactively seek any risk acceptances and be included in the loop for any risk-based decisions or changes to risk appetite. It is likely that cyber risk is being driven in full or in part by your CISO (and maybe General Counsel / CLO) and that CISO may be gapping in your skills to be able to determine what the real inherent or residual risk you introduce by your decisions. This is the same reason to bring in your legal team – likely they are responsible for writing Master Services Agreements (MSAs), answering 3rd party questionnaires and assessing 3rd party risk. It is helpful to talk to them in plain terms about what your 11-stage pipeline brings (“We are able to reduce or eliminate all vulnerabilities in our cloud environment and software packages”) and how they can answer a questionnaire. You can also help them with evaluating a new commercial tool you can bring in or even lend your expertise to writing more stringent MSAs or reviewing one sent by a 3rd party (customer or another business) who consumes your services.

/opinion time over