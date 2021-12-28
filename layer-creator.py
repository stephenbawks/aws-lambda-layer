#!/usr/bin/python

import os
import boto3
from botocore.exceptions import ClientError
import argparse


"""
    Creates a AWS Lambda Layer

    Returns:
        Status of the operation
"""

parser = argparse.ArgumentParser(description="Check for AWS SSM Parameter")

parser.add_argument("--layerdirectory", metavar='layerdirectory', type=str, help="Working directory in repository where requirements file exists")
parser.add_argument("--runtime", metavar='runtime', type=str, help="AWS Lambda Runtime")
parser.add_argument("--bucketname", metavar='bucketname', type=str, help="AWS S3 Bucket Name where layer will be uploaded")

args = parser.parse_args()


def create_zip(lambda_runtime: str, working_directory: str):
            
    SANITIZED_LAMBDA_RUNTIME = lambda_runtime.lower()
    if SANITIZED_LAMBDA_RUNTIME == "nodejs14.x" or SANITIZED_LAMBDA_RUNTIME == "nodejs12.x" or SANITIZED_LAMBDA_RUNTIME == "nodejs10.x":
        CURRENT_RUNTIME == "NODE"
        FOLDER_PATH = "nodejs/node_modules"
    elif SANITIZED_LAMBDA_RUNTIME == "python3.9" or SANITIZED_LAMBDA_RUNTIME == "python3.8" or SANITIZED_LAMBDA_RUNTIME == "python3.7" or SANITIZED_LAMBDA_RUNTIME == "python3.6" or SANITIZED_LAMBDA_RUNTIME == "python2.7":
        CURRENT_RUNTIME == "PYTHON3"
        FOLDER_PATH = "python"
    elif SANITIZED_LAMBDA_RUNTIME == "java11" or SANITIZED_LAMBDA_RUNTIME == "java8.al2" or SANITIZED_LAMBDA_RUNTIME == "java8":
        CURRENT_RUNTIME == "JAVA"
        FOLDER_PATH == "java/lib"
    elif SANITIZED_LAMBDA_RUNTIME == "go1.x":
        CURRENT_RUNTIME == "GO"
        FOLDER_PATH == "bin"

    path = os.path.join(working_directory, FOLDER_PATH)
    os.mkdir(path)

    mkdir -p python/lib/python3.9/site-packages && pip install -r requirements.txt -t ./python/lib/python3.9/site-packages

    zip -r lambda_layer.zip ./python



def create_lambda_layer(parameter_name: str, parameter_value: str, parameter_description: str, parameter_tier: str) -> bool:
    """
    Check to see if the value of a AWS SSM Parameter is up to date
    
    URLs:
        - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.describe_parameters
        - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_parameter
    Parameters:
        parameter_name (str): AWS SSM Parameter Name
        parameter_value (str): AWS SSM Parameter Value
        parameter_description (str): Optional AWS SSM Parameter Description
        parameter_tier (str): Optional The parameter tier to assign to a parameter.
    Returns:
        True or False (bool): [Value of the SSM parameter for the client token]
    """

    try:
        response = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
        value = response['Parameter']['Value']
        print("Parameter Exists, checking parameter details....")
        print(f" - Parameter Value: {parameter_name}")

        parameter_details = ssm.describe_parameters(
            ParameterFilters=[
                {
                    'Key': 'Name',
                    'Values': [parameter_name]
                },
            ],
        )
        
        try:
            description = parameter_details['Parameters'][0]['Description']
        except KeyError:
            print('Description not found')
            description = ''
        
        tier = parameter_details['Parameters'][0]['Tier']

        if value == parameter_value and description == parameter_description and tier == parameter_tier:
            print(" - Verified parameter details are current.")
            return True
        else:
            print(" - Parameter details need to be updated.")
            return False
    except ClientError as e:
        # If the parameter does not exist, return None
        if e.response['Error']['Code'] == 'ParameterNotFound':
            print("Parameter does not exist and needs to be created.")
            return False
        else:
            raise



    DATE=$(date +"%d_%m_%Y")
    FOLDER_PATH="nonprod/${LAYER_NAME_PREFIX}/${DATE}"
    LAYER_NAME="${LAYER_NAME_PREFIX}-${DATE}"

    aws s3 cp ./lambda_layer.zip s3://${BUCKET_NAME}/${FOLDER_PATH}/lambda_layer.zip
          response=$(aws lambda publish-layer-version --layer-name ${LAYER_NAME} \
          --description "Python Development Layer" \
          --content S3Bucket=${BUCKET_NAME},S3Key=${FOLDER_PATH}/lambda_layer.zip \
          --compatible-runtimes "python3.8" "python3.9")
          layer_version=$(echo $response | jq -r '.Version')
          echo "::set-output name=layer_version::$(echo $response | jq -r '.Version')"
          echo "::set-output name=layer_arn::$(echo $response | jq -r '.LayerArn')"
          echo "::set-output name=layer_name::${LAYER_NAME}"
      - name: Lambda Layer Permission
        run: |
          ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
          aws lambda add-layer-version-permission --layer-name ${{ steps.build-layer.outputs.layer_name }} \
          --version-number ${{ steps.build-layer.outputs.layer_version }} --action lambda:GetLayerVersion \
          --statement-id GrantAccountAccess --principal ${ACCOUNT_ID}