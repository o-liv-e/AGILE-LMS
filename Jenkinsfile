
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

    stages {
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
                    bat '''
                        @echo off
                        powershell -NoProfile -ExecutionPolicy Bypass -Command "$env:DOCKER_TOKEN | docker login -u $env:DOCKER_USER --password-stdin"
                        if errorlevel 1 exit /b 1
                        docker push %IMAGE_NAME%:%VERSION%
                        if errorlevel 1 exit /b 1
                        docker logout
                    '''
                }
            }
        }

    }
}
