import boto3
import sagemaker

# Set up SageMaker session
sess = sagemaker.Session()

# Specify training job parameters
training_params = {
    "AlgorithmSpecification": {
        "TrainingImage": "image-uri",
        "TrainingInputMode": "File",
        "MetricDefinitions": [
            {
                "Name": "train:loss",
                "Regex": "train_loss=([0-9\\.]+)"
            }
        ]
    },
    "RoleArn": "aws_sagemaker_ececution",
    "OutputDataConfig": {
        "S3OutputPath": "s3://sagemakerbucketedurekademo/output"
    },
    "ResourceConfig": {
        "InstanceCount": 1,
        "InstanceType": "ml.m4.xlarge",
        "VolumeSizeInGB": 30
    },
    "StoppingCondition": {
        "MaxRuntimeInSeconds": 86400
    },
    "InputDataConfig": [
        {
            "ChannelName": "training",
            "DataSource": {
                "S3DataSource": {
                    "S3DataType": "S3Prefix",
                    "S3Uri": "s3://sagemakerbucketedurekademo/train_data",
                    "S3DataDistributionType": "FullyReplicated"
                }
            }
        }
    ]
}

# Create SageMaker training job
try:
    training_job_name = "my-training-job"
    sess.sagemaker_client.create_training_job(TrainingJobName=training_job_name, **training_params)
    print(f"Training job '{training_job_name}' successfully created.")
except Exception as e:
    print(f"Error creating training job: {e}")
