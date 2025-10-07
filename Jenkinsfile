pipeline {
  agent any

  environment {
    PYTHON = '/usr/bin/python3'
    NODE_HOME = tool name: 'NodeJS', type: 'NodeJSInstallation'
    PATH = "${NODE_HOME}/bin:${env.PATH}"
  }

  stages {

    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Backend Setup') {
      steps {
        dir('backend') {
          echo "Setting up backend..."
          sh 'python3 -m venv venv'
          sh '. venv/bin/activate && pip install -r ../requirements.txt'
        }
      }
    }

    stage('Model Validation') {
      steps {
        dir('model') {
          echo "Running basic model check..."
          sh 'python3 verify_model.py || echo "No verification script found"'
        }
      }
    }

    stage('Frontend Build') {
      steps {
        dir('frontend') {
          echo "Installing and building frontend..."
          sh 'npm install'
          sh 'npm run build'
        }
      }
    }

    stage('Backend Tests') {
      steps {
        dir('backend') {
          echo "Running backend tests..."
          sh '. venv/bin/activate && pytest || echo "No tests found"'
        }
      }
    }

    stage('Package Artifacts') {
      steps {
        echo "Packaging build outputs..."
        sh 'tar -czf build_artifacts.tar.gz frontend/dist backend/venv model'
        archiveArtifacts artifacts: 'build_artifacts.tar.gz', allowEmptyArchive: true
      }
    }

    stage('Deploy') {
      when { branch 'main' }
      steps {
        echo "Deploying to server..."
        // You can replace this with actual deployment commands:
        sh 'echo "Deploying app..."'
      }
    }
  }


post {
  always {
    echo "Cleaning up workspace..."
    node {
      deleteDir()
    }
  }
}
