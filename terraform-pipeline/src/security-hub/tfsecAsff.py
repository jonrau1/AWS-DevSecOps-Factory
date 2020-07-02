import os
import boto3
import json
import datetime
# import sechub + sts boto3 client
securityhub = boto3.client('securityhub')
sts = boto3.client('sts')
# retrieve account id from STS
awsAccount = sts.get_caller_identity()['Account']
# retrieve env vars from codebuild
awsRegion = os.environ['AWS_REGION']
codebuildBuildArn = os.environ['CODEBUILD_BUILD_ARN']

with open('tfsec-findings.json') as json_file:
    data = json.load(json_file)
    if str(data) == "{'results': None}":
        pass
    else:
        for result in data['results']:
            ruleId = str(result['rule_id'])
            ruleLink = str(result['link'])
            fileName = str(result['location']['filename'])
            startLine = str(result['location']['start_line'])
            endLine = str(result['location']['end_line'])
            ruleDescr = str(result['description'])
            tfsecSev = str(result['severity'])
            try:
                iso8601Time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()        
                response = securityhub.batch_import_findings(
                    Findings=[
                        {
                            'SchemaVersion': '2018-10-08',
                            'Id': codebuildBuildArn + 'tfsec-findings-' + ruleId + '-' + startLine + '-' + endLine,
                            'ProductArn': 'arn:aws:securityhub:' + awsRegion + ':' + awsAccount + ':product/' + awsAccount + '/default',
                            'GeneratorId': codebuildBuildArn,
                            'AwsAccountId': awsAccount,
                            'Types': [ 'Software and Configuration Checks' ],
                            'CreatedAt': iso8601Time,
                            'UpdatedAt': iso8601Time,
                            'Severity': { 
                                'Label': 'LOW',
                                'Original': tfsecSev
                            },
                            'Title': '[TFSec] Security misconfiguration identified in Terraform source files',
                            'Description': 'TFSec has identified security misconfigurations in Terraform source files in source code of build ' + codebuildBuildArn + '. Check ' + ruleId + ' has failed with the following message ' + ruleDescr + ' for filename ' + fileName,
                            'ProductFields': { 
                                'Product Name': 'TFLint'
                            },
                            'Remediation': {
                                'Recommendation': {
                                    'Text': 'For information on the failed check refer to this entry from TFSec',
                                    'Url': ruleLink
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
                                            'ruleId': ruleId,
                                            'ruleDescription': ruleDescr,
                                            'fileName': fileName
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