pipeline {
    agent any

    environment {
        AWS_CREDENTIALS = credentials('aws-credentials') // Ensure this exists in Jenkins
        S3_BUCKET = 'lambda-deployment-cicd'
        FUNCTION_NAME = 'my-lambda-cicd'
        AWS_REGION = 'ap-south-1'  // ✅ Set your region explicitly
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'master', url: 'https://github.com/SefaliSabnam/Lambda-jenkins-cicd.git'
            }
        }

        stage('Package Lambda') {
            steps {
                sh '''
                zip lambda-package.zip lambda_function.py
                '''
            }
        }

        stage('Upload to S3') {
            steps {
                sh '''
                aws s3 cp lambda-package.zip s3://$S3_BUCKET/lambda-package.zip --region $AWS_REGION
                '''
            }
        }

        stage('Deploy to Lambda') {
            steps {
                sh '''
                aws lambda update-function-code \
                --function-name $FUNCTION_NAME \
                --s3-bucket $S3_BUCKET \
                --s3-key lambda-package.zip \
                --region $AWS_REGION
                '''
            }
        }
    }

    post {
        always {
            sh 'rm -f lambda-package.zip'
        }
        success {
            echo '✅ Deployment Successful!'
        }
        failure {
            echo '❌ Deployment Failed! Check logs.'
        }
    }
}
