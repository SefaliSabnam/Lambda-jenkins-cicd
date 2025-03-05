pipeline {
    agent any

    environment {
        AWS_CREDENTIALS = credentials('aws-credentials') // Single credentials ID
        S3_BUCKET = 'pramod-lambda-deployments'
        FUNCTION_NAME = 'myLambdaFunction'
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'master', url: 'https://github.com/PramodaHS/Lambda-jenkins-cicd.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''#!/bin/bash
                set -e  # Exit on error
                mkdir -p package
                if [ -f requirements.txt ]; then
                    pip install -r requirements.txt -t package/
                else
                    echo "Error: requirements.txt not found!"
                    exit 1
                fi
                '''
            }
        }

        stage('Package Lambda') {
            steps {
                sh '''#!/bin/bash
                set -e  # Exit on error
                cd package && zip -r ../lambda-package.zip . || exit 1
                cd .. && zip -g lambda-package.zip lambda_function.py || exit 1
                '''
            }
        }

        stage('Upload to S3') {
            steps {
                sh '''#!/bin/bash
                set -e  # Exit on error
                aws s3 cp lambda-package.zip s3://$S3_BUCKET/lambda-package.zip
                '''
            }
        }

        stage('Deploy to Lambda') {
            steps {
                sh '''#!/bin/bash
                set -e  # Exit on error
                aws lambda update-function-code \
                --function-name $FUNCTION_NAME \
                --s3-bucket $S3_BUCKET \
                --s3-key lambda-package.zip
                '''
            }
        }
    }

    post {
        always {
            sh 'rm -f lambda-package.zip'
            sh 'rm -rf package'
        }
        success {
            echo '✅ Deployment Successful!'
        }
        failure {
            echo '❌ Deployment Failed! Check logs.'
        }
    }
}
