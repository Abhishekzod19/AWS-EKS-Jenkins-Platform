pipeline {
    agent any

    environment {
        AWS_REGION = 'eu-west-1'
        AWS_ACCOUNT_ID = '357542025142'
        ECR_REPO = 'demo-app'
        IMAGE_TAG = "${BUILD_NUMBER}"
        ECR_URI = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}"
        CLUSTER_NAME = 'demo-eks-cluster'
        NAMESPACE = 'demo-app'
        DEPLOYMENT_NAME = 'demo-app'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build AMD64 Docker Image') {
            steps {
                sh '''
                docker buildx build \
                  --platform linux/amd64 \
                  -t ${ECR_REPO}:${IMAGE_TAG} \
                  -t ${ECR_URI}:${IMAGE_TAG} \
                  -t ${ECR_URI}:latest \
                  --load \
                  ./app
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

        stage('Update Kubeconfig') {
            steps {
                sh '''
                aws eks update-kubeconfig \
                  --region ${AWS_REGION} \
                  --name ${CLUSTER_NAME}
                '''
            }
        }

        stage('Deploy to EKS') {
            steps {
                sh '''
                kubectl set image deployment/${DEPLOYMENT_NAME} \
                  demo-app=${ECR_URI}:${IMAGE_TAG} \
                  -n ${NAMESPACE}

                kubectl rollout status deployment/${DEPLOYMENT_NAME} \
                  -n ${NAMESPACE}
                '''
            }
        }
    }

    post {
        success {
            echo 'CI/CD completed: image pushed to ECR and deployed to EKS.'
        }

        failure {
            echo 'Pipeline failed. Check console output.'
        }
    }
}