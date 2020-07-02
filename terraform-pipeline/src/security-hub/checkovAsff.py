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

with open('checkov-findings.json') as json_file:
    data = json.load(json_file)
    checkTest = str(data['results']['failed_checks'])
    if checkTest == '[]':
        pass
    else:
        for checks in data['results']['failed_checks']:
            checkId = str(checks['check_id'])
            checkName = str(checks['check_name'])
            checkovSev = str(checks['check_result']['result'])
            fileName = str(checks['file_path'])
            tfResource = str(checks['resource'])
            reccoUrl = str(checks['guideline'])
            try:
                iso8601Time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()        
                response = securityhub.batch_import_findings(
                    Findings=[
                        {
                            'SchemaVersion': '2018-10-08',
                            'Id': codebuildBuildArn + 'checkov-findings-' + checkId + '-' + tfResource,
                            'ProductArn': 'arn:aws:securityhub:' + awsRegion + ':' + awsAccount + ':product/' + awsAccount + '/default',
                            'GeneratorId': codebuildBuildArn,
                            'AwsAccountId': awsAccount,
                            'Types': [ 'Software and Configuration Checks' ],
                            'CreatedAt': iso8601Time,
                            'UpdatedAt': iso8601Time,
                            'Severity': { 
                                'Label': 'LOW',
                                'Original': checkovSev
                            },
                            'Title': '[Checkov] Security misconfiguration identified in Terraform source files',
                            'Description': 'Checkov has identified security misconfigurations in Terraform source files in source code of build ' + codebuildBuildArn + '. Check ' + checkId + ' has failed with the following message ' + checkName + ' for filename ' + fileName,
                            'ProductFields': { 
                                'Product Name': 'TFLint'
                            },
                            'Remediation': {
                                'Recommendation': {
                                    'Text': 'For information on the Checkov failed check refer to this guideline from Bridgecrew',
                                    'Url': reccoUrl
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
                                            'checkId': checkId,
                                            'checkName': checkName,
                                            'fileName': fileName,
                                            'tfResource': tfResource
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