pipeline {
    agent any
    tools {
        nodejs 'NodeJS'  // Make sure this matches the name in Jenkins configuration
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
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
            cleanWs()  // Use cleanWs instead of deleteDir for better workspace cleanup
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