pipeline {
    agent any
    tools {
        nodejs 'NodeJS'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Check Files') {
            steps {
                script {
                    // List all files in the workspace to see what's actually there
                    bat 'dir /B'
                    bat 'tree /F /A'
                }
            }
        }
        
        stage('Install Dependencies') {
            steps {
                script {
                    bat 'npm install'
                }
            }
        }
        
        stage('Build') {
            steps {
                script {
                    bat 'npm run build'
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    bat 'npm test'
                }
            }
        }
    }
    post {
        always {
            cleanWs()
        }
        failure {
            emailext (
                subject: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                body: "Check console output at ${env.BUILD_URL}",
                to: "vigneshgone043@gmail.com"
            )
        }
    }
}