pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
    }

    stages {

        stage('Checkout Code (SSH)') {
            steps {
                git branch: 'main',
                    url: 'git@github.com:disha-cyber/agentic-ai.git'
            }
        }

        stage('Verify') {
            steps {
                sh 'ls -la'
            }
        }
    }
}
