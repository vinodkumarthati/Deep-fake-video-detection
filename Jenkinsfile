pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                nodejs('NodeJS') {
                    bat 'npm install'
                }
            }
        }
        
        stage('Build') {
            steps {
                nodejs('NodeJS') {
                    bat 'npm run build'
                }
            }
        }
        
        stage('Test') {
            steps {
                nodejs('NodeJS') {
                    bat 'npm test'
                }
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}