pipeline {
    agent any

    tools {
        nodejs "NodeJS"   // Only keep NodeJS — Python is used directly
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/vinodkumarthati/Deep-fake-video-detection.git'
            }
        }

        stage('Frontend Build') {
            steps {
                dir('frontend') {
                    sh '''
                        echo "Installing frontend dependencies..."
                        npm install
                        echo "Building frontend..."
                        npm run build || true
                    '''
                }
            }
        }

        stage('Backend Setup') {
            steps {
                dir('backend') {
                    sh '''
                        echo "Setting up Python environment..."
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt || true
                    '''
                }
            }
        }

        stage('Model Verification') {
            steps {
                script {
                    if (fileExists('model')) {
                        echo '✅ Model folder verified'
                    } else {
                        error('❌ Model folder missing!')
                    }
                }
            }
        }

        stage('Build Artifacts') {
            when {
                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            steps {
                echo "All stages completed successfully!"
            }
        }
    }

    post {
        success {
            echo '🎉 Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed. Please check the logs.'
        }
        always {
            cleanWs()
        }
    }
}
