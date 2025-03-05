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
                aws s3 cp lambda-package.zip s3://$S3_BUCKET/lambda-package.zip
                '''
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
