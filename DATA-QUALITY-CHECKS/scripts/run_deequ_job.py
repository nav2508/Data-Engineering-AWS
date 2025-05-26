import boto3

def run_deequ_job():
    emr = boto3.client('emr')
    response = emr.add_job_flow_steps(
        JobFlowId='j-LLK1AYXPEJQT',
        Steps=[{
            'Name': 'Run Deequ Validation',
            'ActionOnFailure': 'CONTINUE',
            'HadoopJarStep': {
                'Jar': 'command-runner.jar',
                'Args': [
                    'spark-submit',
                    '--deploy-mode', 'cluster',
                    's3://data-validation-and-quality-checks/scripts/quality_check.scala'
                ]
            }
        }]
    )
    print("Step ID: ", response['StepIds'][0])

if __name__ == '__main__':
    run_deequ_job()