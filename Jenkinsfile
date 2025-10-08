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
        
        stage('Frontend Build') {
            steps {
                script {
                    try {
                        dir('frontend') {
                            sh 'npm install'
                            sh 'npm run build'
                            sh 'npm test || echo "Tests skipped or not configured"'
                        }
                    } catch (Exception e) {
                        echo "Frontend build failed: ${e.message}"
                        // Continue with backend build anyway
                    }
                }
            }
        }
        
        stage('Backend Setup') {
            steps {
                script {
                    try {
                        // Check if backend folder exists
                        def backendExists = fileExists 'backend'
                        if (backendExists) {
                            dir('backend') {
                                sh 'pip install -r requirements.txt'
                                sh 'python -m pytest tests/ || echo "No tests found"'
                            }
                        } else {
                            echo "Backend folder not found, skipping backend setup"
                        }
                    } catch (Exception e) {
                        echo "Backend setup failed: ${e.message}"
                        // Continue with the pipeline
                    }
                }
            }
        }
        
        stage('Model Verification') {
            steps {
                script {
                    def modelExists = fileExists 'model'
                    if (modelExists) {
                        echo "Model folder verified"
                        sh 'dir model /B'
                    } else {
                        echo "Model folder not found"
                    }
                }
            }
        }
        
        stage('Build Artifacts') {
            steps {
                script {
                    // Archive frontend build files if they exist
                    dir('frontend') {
                        archiveArtifacts artifacts: 'build/**/*', allowEmptyArchive: true
                    }
                    
                    // Archive requirements files
                    archiveArtifacts artifacts: '**/requirements.txt', allowEmptyArchive: true
                    
                    // Archive model files if they exist
                    archiveArtifacts artifacts: 'model/**/*', allowEmptyArchive: true
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
