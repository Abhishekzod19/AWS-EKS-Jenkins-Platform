pipeline {
    agent any

    environment {
        AWS_REGION = 'eu-west-1'
        AWS_ACCOUNT_ID = '357542025142'
        ECR_REPO = 'demo-app'
        IMAGE_TAG = "${BUILD_NUMBER}"
        ECR_URI = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}"
    }

    stages {

        stage('Build Docker Image') {
            steps {
                sh '''
                cd app

                docker build -t ${ECR_REPO}:${IMAGE_TAG} .

                docker tag ${ECR_REPO}:${IMAGE_TAG} ${ECR_URI}:${IMAGE_TAG}

                docker tag ${ECR_REPO}:${IMAGE_TAG} ${ECR_URI}:latest
                '''
            }
        }

        stage('Login to AWS ECR') {
            steps {
                sh '''
                aws ecr get-login-password --region ${AWS_REGION} | \
                docker login --username AWS --password-stdin \
                ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
                '''
            }
        }

        stage('Push Image to ECR') {
            steps {
                sh '''
                docker push ${ECR_URI}:${IMAGE_TAG}

                docker push ${ECR_URI}:latest
                '''
            }
        }
    }

    post {
        success {
            echo 'Docker image pushed successfully to AWS ECR'
        }

        failure {
            echo 'Pipeline failed'
        }
    }
}
