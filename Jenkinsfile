
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'oliveprishita/lms'
    }

    stages {
        stage('Test') {
            steps {
                bat 'python -m pip install -r requirements.txt'
                bat 'python -m pytest -q'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    if (!(env.BRANCH_NAME in ['v1', 'v2', 'v3'])) {
                        error('Build only from v1, v2, or v3 branches')
                    }
                }

                bat 'docker build -t %IMAGE_NAME%:%BRANCH_NAME% .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_TOKEN'
                )]) {
                    bat 'echo %DOCKER_TOKEN% | docker login -u %DOCKER_USER% --password-stdin'
                    bat 'docker push %IMAGE_NAME%:%BRANCH_NAME%'
                    bat 'docker logout'
                }
            }
        }
    }
}
