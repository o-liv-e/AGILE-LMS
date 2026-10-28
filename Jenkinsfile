
pipeline {
    agent any

    parameters {
        choice(
            name: 'VERSION',
            choices: ['v1', 'v2', 'v3'],
            description: 'Select the LMS version to build'
        )
    }

    environment {
        IMAGE_NAME = 'oliveprishita/lms'
    }

    stage('Checkout Selected Version') {
    steps {
        checkout([
            $class: 'GitSCM',
            branches: [[name: "*/${params.VERSION}"]],
            userRemoteConfigs: [[
                url: 'https://github.com/o-liv-e/AGILE-LMS.git'
            ]]
        ])
    }
}
        stage('Test') {
            steps {
                bat 'python -m pip install -r requirements.txt'
                bat 'python -m pytest -q'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME%:%VERSION% .'
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
                    bat 'docker push %IMAGE_NAME%:%VERSION%'
                    bat 'docker logout'
                }
            }
        }
    }
}
