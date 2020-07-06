import json
import boto3
import datetime
import os
# import sechub + sts boto3 client
securityhub = boto3.client('securityhub')
sts = boto3.client('sts')
# retrieve account id from STS
awsAccount = sts.get_caller_identity()['Account']
# retrieve env vars from codebuild
awsRegion = os.environ['AWS_REGION']
codebuildBuildArn = os.environ['CODEBUILD_BUILD_ARN']

with open('skan-findings.json') as json_file:
    data = json.load(json_file)
    for key in data['Reports']:
        for findings in data['Reports'][key]['Results']:
            checkCategory = str(findings['Category'])
            checkModule = str(findings['Check']['ModuleId'])
            checkGroup = str(findings['Check']['GroupId'])
            checkNum = str(findings['Check']['CheckId'])
            newCheckId = checkModule + '.' + checkGroup + '.' + checkNum
            checkName = str(findings['Check']['CheckTitle'])
            checkDescription = str(findings['Message'])
            checkDescription = (checkDescription[:700] + '..') if len(checkDescription) > 700 else checkDescription
            reccDescription = str(findings['Message'])
            reccDescription = (reccDescription[:1000] + '..') if len(reccDescription) > 1000 else reccDescription
            reccLink = str(findings['References'][0])
            skanSev = str(findings['Severity'])
            if skanSev == 'Critical':
                shSev = 'CRITICAL'
            elif skanSev == 'High':
                shSev = 'HIGH'
            elif skanSev == 'Medium':
                shSev = 'MEDIUM'
            else:
                shSev = 'LOW'
            try:
                iso8601Time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()        
                response = securityhub.batch_import_findings(
                    Findings=[
                        {
                            'SchemaVersion': '2018-10-08',
                            'Id': codebuildBuildArn + 'sKan-scan' + newCheckId,
                            'ProductArn': 'arn:aws:securityhub:' + awsRegion + ':' + awsAccount + ':product/' + awsAccount + '/default',
                            'GeneratorId': codebuildBuildArn,
                            'AwsAccountId': awsAccount,
                            'Types': [ 'Software and Configuration Checks' ],
                            'CreatedAt': iso8601Time,
                            'UpdatedAt': iso8601Time,
                            'Severity': { 
                                'Label': shSev,
                                'Original': skanSev
                            },
                            'Title': '[sKan] Security misconfigurations identified in Kubernetes configuration file or Helm Chart',
                            'Description': 'Alcide sKan identified security misconfigurations in Kubernetes configuration file or Helm Chart during build ' + codebuildBuildArn + ' with the following information (may be truncated): ' + checkDescription,
                            'ProductFields': { 
                                'Product Name': 'sKan'
                            },
                            'Remediation': {
                                'Recommendation': {
                                    'Text': reccDescription,
                                    'Url': reccLink
                                }
                            },
                            'Resources': [
                                {
                                    'Type': 'AwsCodeBuildProject',
                                    'Id': codebuildBuildArn,
                                    'Partition': 'aws',
                                    'Region': awsRegion,
                                    'Details': {
                                        'AwsCodeBuildProject': { 'Name': codebuildBuildArn },
                                        'Other': {
                                            'findingId': newCheckId,
                                            'findingName': checkName,
                                            'findingCategory': checkCategory
                                        }
                                    }
                                }
                            ],
                            'RecordState': 'ACTIVE',
                            'Workflow': {'Status': 'NEW'}
                        }
                    ]
                )
                print(response)
            except Exception as e:
                print(e)