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

with open('polaris-findings.json') as json_file:
    data = json.load(json_file)
    sourceName = str(data['SourceName'])

def pod_findings():
    for r in data['Results']:
        for key in r['PodResult']['Results']:
            if str(r['PodResult']['Results'][key]['Success']) == 'False':
                findingId = r['PodResult']['Results'][key]['ID']
                findingDescription = r['PodResult']['Results'][key]['Message']
                findingCategory = r['PodResult']['Results'][key]['Category']
                polarisSev = r['PodResult']['Results'][key]['Severity']
                try:
                    iso8601Time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()        
                    response = securityhub.batch_import_findings(
                        Findings=[
                            {
                                'SchemaVersion': '2018-10-08',
                                'Id': codebuildBuildArn + 'polaris-scan' + findingId,
                                'ProductArn': 'arn:aws:securityhub:' + awsRegion + ':' + awsAccount + ':product/' + awsAccount + '/default',
                                'GeneratorId': codebuildBuildArn,
                                'AwsAccountId': awsAccount,
                                'Types': [ 'Software and Configuration Checks' ],
                                'CreatedAt': iso8601Time,
                                'UpdatedAt': iso8601Time,
                                'Severity': { 
                                    'Label': 'MEDIUM',
                                    'Original': polarisSev
                                },
                                'Title': '[Polaris] Security or network misconfigurations identified in Kubernetes configuration file or Helm Chart',
                                'Description': 'Detect-Secrets identified security or network misconfigurations in Kubernetes configuration file or Helm Chart during build ' + codebuildBuildArn + '. The following check in the ' + findingCategory + ' category failed: ' + findingDescription,
                                'ProductFields': { 
                                    'Product Name': 'Polaris'
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
                                                'findingId': findingId,
                                                'findingCategory': findingCategory,
                                                'sourceName': sourceName
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
            else:
                pass

def container_findings():
    for r in data['Results']:
        for c in r['PodResult']['ContainerResults']:
            for key in c['Results']:
                if str(c['Results'][key]['Success']) == 'False':
                    findingId = c['Results'][key]['ID']
                    findingDescription = c['Results'][key]['Message']
                    findingCategory = c['Results'][key]['Category']
                    polarisSev = c['Results'][key]['Severity']
                    try:
                        iso8601Time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()        
                        response = securityhub.batch_import_findings(
                            Findings=[
                                {
                                    'SchemaVersion': '2018-10-08',
                                    'Id': codebuildBuildArn + 'polaris-scan' + findingId,
                                    'ProductArn': 'arn:aws:securityhub:' + awsRegion + ':' + awsAccount + ':product/' + awsAccount + '/default',
                                    'GeneratorId': codebuildBuildArn,
                                    'AwsAccountId': awsAccount,
                                    'Types': [ 'Software and Configuration Checks' ],
                                    'CreatedAt': iso8601Time,
                                    'UpdatedAt': iso8601Time,
                                    'Severity': { 
                                        'Label': 'MEDIUM',
                                        'Original': polarisSev
                                    },
                                    'Title': '[Polaris] Security or network misconfigurations identified in Kubernetes configuration file or Helm Chart',
                                    'Description': 'Detect-Secrets identified security or network misconfigurations in Kubernetes configuration file or Helm Chart during build ' + codebuildBuildArn + '. The following check in the ' + findingCategory + ' category failed: ' + findingDescription,
                                    'ProductFields': { 
                                        'Product Name': 'Polaris'
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
                                                    'findingId': findingId,
                                                    'findingCategory': findingCategory,
                                                    'sourceName': sourceName
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
                else:
                    pass

def main():
    pod_findings()
    container_findings()

main()