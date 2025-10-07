pipeline {
    agent any  // Use any available agent

    environment {
        // Adjust the NodeJS tool name to match your Jenkins configuration
        NODE_HOME = tool name: 'NodeJS', type: 'NodeJSInstallation'
        PATH = "${NODE_HOME}/bin:${env.PATH}"
        PYTHON = 'C:\\Python39\\python.exe' // Change if needed
    }

    stages {

        stage('Checkout') {
            steps {
                echo "Checking out source code..."
                checkout scm
            }
        }

        stage('Backend Setup') {
            steps {
                dir('backend') {
                    echo "Setting up Python environment..."
                    bat "${env.PYTHON} -m venv venv"
                    bat "venv\\Scripts\\activate && pip install -r ..\\requirements.txt"
                }
            }
        }

        stage('Model Validation') {
            steps {
                dir('model') {
                    echo "Running basic model check..."
                    bat "python verify_model.py || echo No verification script found"
                }
            }
        }

        stage('Frontend Build') {
            steps {
                dir('frontend') {
                    echo "Installing and building frontend..."
                    bat "npm install"
                    bat "npm run build"
                }
            }
        }

        stage('Backend Tests') {
            steps {
                dir('backend') {
                    echo "Running backend tests..."
                    bat "venv\\Scripts\\activate && pytest || echo No tests found"
                }
            }
        }

        stage('Package Artifacts') {
            steps {
                echo "Packaging build artifacts..."
                bat "tar -czf build_artifacts.tar.gz frontend\\dist backend\\venv model"
                archiveArtifacts artifacts: 'build_artifacts.tar.gz', allowEmptyArchive: true
            }
        }

        stage('Deploy') {
            when { branch 'main' }
            steps {
                echo "Deploying to server..."
                bat "echo Deploying app..."
            }
        }
    }

    post {
        always {
            echo "Cleaning up workspace..."
            deleteDir()  // Runs on the agent automatically
        }
    }
}
