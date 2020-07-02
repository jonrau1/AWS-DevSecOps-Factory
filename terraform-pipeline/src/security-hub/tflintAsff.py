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

with open('tflint-findings.json') as json_file:
    data = json.load(json_file)
    lintIssues = str(data['issues'])
    if lintIssues == '[]':
        pass
    else:
        try:
            iso8601Time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()        
            response = securityhub.batch_import_findings(
                Findings=[
                    {
                        'SchemaVersion': '2018-10-08',
                        'Id': codebuildBuildArn + 'tflint-findings',
                        'ProductArn': 'arn:aws:securityhub:' + awsRegion + ':' + awsAccount + ':product/' + awsAccount + '/default',
                        'GeneratorId': codebuildBuildArn,
                        'AwsAccountId': awsAccount,
                        'Types': [ 'Software and Configuration Checks' ],
                        'CreatedAt': iso8601Time,
                        'UpdatedAt': iso8601Time,
                        'Severity': { 'Label': 'LOW' },
                        'Title': '[TFLint] Syntax or security issues identified in Terraform source files',
                        'Description': 'TFLint has identified syntax or security issues identified in Terraform source files in source code of build ' + codebuildBuildArn + ' refer to the CodeBuild logs to view any issues that were found.',
                        'ProductFields': { 
                            'Product Name': 'TFLint'
                        },
                        'Resources': [
                            {
                                'Type': 'AwsCodeBuildProject',
                                'Id': codebuildBuildArn,
                                'Partition': 'aws',
                                'Region': awsRegion,
                                'Details': {
                                    'AwsCodeBuildProject': { 'Name': codebuildBuildArn }
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
    lintErrors = str(data['errors'])
    if lintErrors == '[]':
        pass
    else:
        try:
            iso8601Time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()        
            response = securityhub.batch_import_findings(
                Findings=[
                    {
                        'SchemaVersion': '2018-10-08',
                        'Id': codebuildBuildArn + 'tflint-findings',
                        'ProductArn': 'arn:aws:securityhub:' + awsRegion + ':' + awsAccount + ':product/' + awsAccount + '/default',
                        'GeneratorId': codebuildBuildArn,
                        'AwsAccountId': awsAccount,
                        'Types': [ 'Software and Configuration Checks' ],
                        'CreatedAt': iso8601Time,
                        'UpdatedAt': iso8601Time,
                        'Severity': { 'Label': 'MEDIUM' },
                        'Title': '[TFLint] Syntax or security errors identified in Terraform source files',
                        'Description': 'TFLint has identified syntax or security errors identified in Terraform source files in source code of build ' + codebuildBuildArn + ' refer to the CodeBuild logs to view any issues that were found.',
                        'ProductFields': { 
                            'Product Name': 'TFLint'
                        },
                        'Resources': [
                            {
                                'Type': 'AwsCodeBuildProject',
                                'Id': codebuildBuildArn,
                                'Partition': 'aws',
                                'Region': awsRegion,
                                'Details': {
                                    'AwsCodeBuildProject': { 'Name': codebuildBuildArn }
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