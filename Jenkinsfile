pipeline {
    agent any

    environment {
        S3_BUCKET = 'lambda-deployment-cicd'
        FUNCTION_NAME = 'my-lambda-cicd'
        AWS_REGION = 'ap-south-1'  // ✅ Set your region explicitly
    }

    stages {
        stage('Checkout Code') {
            steps {
                script {
                    //  Added credentialsId for GitHub authentication
                    checkout([$class: 'GitSCM',
                              branches: [[name: '*/UA-0209']],
                              userRemoteConfigs: [[url: 'https://github.com/SefaliSabnam/Lambda-jenkins-cicd.git',
                                                   credentialsId: 'github-credentials']]
                    ])
                }
            }
        }

        stage('Package Lambda') {
            steps {
                script {
                    node {
                        sh '''
                        zip lambda-package.zip lambda_function.py
                        '''
                    }
                }
            }
        }

        stage('Upload to S3') {
            steps {
                script {
                    node {
                        withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-credentials']]) {
                            sh '''
                            aws s3 cp lambda-package.zip s3://$S3_BUCKET/lambda-package.zip --region $AWS_REGION
                            '''
                        }
                    }
                }
            }
        }

        stage('Deploy to Lambda') {
            steps {
                script {
                    node {
                        withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-credentials']]) {
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
            }
        }
    }

    post {
        always {
            script {
                node {
                    sh 'rm -f lambda-package.zip'
                }
            }
        }
        success {
            echo ' Deployment Successful!'
        }
        failure {
            echo ' Deployment Failed! Check logs.'
        }
    }
}
