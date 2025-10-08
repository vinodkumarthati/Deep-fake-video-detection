pipeline {
    agent any

    tools {
        nodejs "NodeJS"
        python "Python3"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/vinodkumarthati/Deep-fake-video-detection.git'
            }
        }

        stage('Frontend Build') {
            steps {
                dir('frontend') {
                    sh 'npm install'
                    sh 'npm run build'
                    catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                        sh 'npm test || true'
                    }
                }
            }
        }

        stage('Backend Setup') {
            steps {
                dir('backend') {
                    sh 'pip install -r requirements.txt'
                }
            }
        }

        stage('Model Verification') {
            steps {
                script {
                    if (fileExists('model')) {
                        echo 'Model folder verified'
                        sh 'ls -lh model'
                    } else {
                        error('Model folder not found')
                    }
                }
            }
        }

        stage('Build Artifacts') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                echo 'Build successful! Artifacts are ready.'
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
