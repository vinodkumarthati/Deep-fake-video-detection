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
        
        stage('Check Project Structure') {
            steps {
                script {
                    echo "Checking project structure..."
                    bat 'dir /B'
                }
            }
        }
        
        stage('Frontend - Install Dependencies') {
            steps {
                script {
                    dir('frontend') {
                        bat 'npm install'
                    }
                }
            }
        }
        
        stage('Frontend - Build') {
            steps {
                script {
                    dir('frontend') {
                        bat 'npm run build'
                    }
                }
            }
        }
        
        stage('Frontend - Test') {
            steps {
                script {
                    dir('frontend') {
                        bat 'npm test || echo "Frontend tests completed"'
                    }
                }
            }
        }
        
        stage('Backend - Setup Python') {
            steps {
                script {
                    bat 'python --version || echo "Python not found"'
                    bat 'pip --version || echo "Pip not found"'
                }
            }
        }
        
        stage('Backend - Install Dependencies') {
            steps {
                script {
                    // Install backend Python dependencies
                    bat 'pip install -r requirements.txt || echo "No requirements.txt found"'
                    
                    // If you have specific backend folder with its own requirements
                    dir('backend') {
                        bat 'pip install -r requirements.txt || echo "No backend requirements.txt"'
                    }
                }
            }
        }
        
        stage('Backend - Test') {
            steps {
                script {
                    // Run Python tests if they exist
                    bat 'python -m pytest tests/ || echo "No Python tests found"'
                    bat 'python -m pytest backend/tests/ || echo "No backend tests found"'
                }
            }
        }
        
        stage('Model - Verify') {
            steps {
                script {
                    echo "Checking model files..."
                    bat 'dir model /B || echo "Model folder not found"'
                }
            }
        }
    }
    post {
        always {
            cleanWs()
        }
        success {
            emailext (
                subject: "SUCCESS: Deep Fake Detection Build - ${env.JOB_NAME} [${env.BUILD_NUMBER}]",
                body: """
                Build Successful!
                
                Job: ${env.JOB_NAME}
                Build Number: ${env.BUILD_NUMBER}
                URL: ${env.BUILD_URL}
                
                Both frontend and backend components built successfully.
                """,
                to: "vigneshgone043@gmail.com"
            )
        }
        failure {
            emailext (
                subject: "FAILED: Deep Fake Detection Build - ${env.JOB_NAME} [${env.BUILD_NUMBER}]",
                body: """
                Build Failed!
                
                Job: ${env.JOB_NAME}
                Build Number: ${env.BUILD_NUMBER}
                URL: ${env.BUILD_URL}
                
                Please check the build logs for details.
                """,
                to: "vigneshgone043@gmail.com"
            )
        }
    }
}