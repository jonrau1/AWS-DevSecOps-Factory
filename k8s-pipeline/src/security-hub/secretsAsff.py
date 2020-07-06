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
try:
    with open('secret-results.json') as json_file:
        data = json.load(json_file)
        if str(data['results']) == '{}':
            pass
        else:
            secretDetectionCheck = str(data['results'])
            secretDetectionCheck = (secretDetectionCheck[:700] + '..') if len(secretDetectionCheck) > 700 else secretDetectionCheck
            secretTimestamp = str(data['generated_at'])
            try:
                iso8601Time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()        
                response = securityhub.batch_import_findings(
                    Findings=[
                        {
                            'SchemaVersion': '2018-10-08',
                            'Id': codebuildBuildArn + 'detect-secrets-scan' + secretTimestamp,
                            'ProductArn': 'arn:aws:securityhub:' + awsRegion + ':' + awsAccount + ':product/' + awsAccount + '/default',
                            'GeneratorId': codebuildBuildArn,
                            'AwsAccountId': awsAccount,
                            'Types': [ 
                                'Sensitive Data Identifications',
                                'Effects/Data Exposure' 
                            ],
                            'CreatedAt': iso8601Time,
                            'UpdatedAt': iso8601Time,
                            'Severity': { 'Label': 'CRITICAL' },
                            'Title': 'Detect-Secrets identified sensitive information in source code',
                            'Description': 'Detect-Secrets identified sensitive information in source code of build ' + codebuildBuildArn + ' with the following information (may be truncated): ' + secretDetectionCheck,
                            'ProductFields': { 
                                'Product Name': 'Detect-Secrets'
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
except Exception as e:
    print(e)