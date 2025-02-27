pipeline {
    agent any

    environment {
        AWS_ACCESS_KEY_ID = credentials('aws-credentials')
        AWS_SECRET_ACCESS_KEY = credentials('aws-credentials')
        S3_BUCKET = 'pramod-lambda-deployments'
        FUNCTION_NAME = 'myLambdaFunction'
    }

    stages {
        stage('Checkout Code') {
            steps {
                git 'https://github.com/your-username/lambda-cicd.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt -t package/'
            }
        }

        stage('Package Lambda') {
            steps {
                sh 'cd package && zip -r ../lambda-package.zip .'
                sh 'zip -g lambda-package.zip lambda_function.py'
            }
        }

        stage('Upload to S3') {
            steps {
                sh 'aws s3 cp lambda-package.zip s3://$S3_BUCKET/'
            }
        }

        stage('Deploy to Lambda') {
            steps {
                sh '''
                aws lambda update-function-code \
                --function-name $FUNCTION_NAME \
                --s3-bucket $S3_BUCKET \
                --s3-key lambda-package.zip
                '''
            }
        }
    }
}
