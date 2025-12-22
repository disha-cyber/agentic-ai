pipeline {
    agent any

    options {
        skipDefaultCheckout(true)   // 🚨 CRITICAL
    }

    stages {

        stage('Checkout Code via SSH (Should Fail)') {
            steps {
                git branch: 'main',
                    url: 'git@github.com:disha-cyber/agentic-ai.git'
                    // ❌ NO credentialsId on purpose
            }
        }

        stage('Verify') {
            steps {
                sh 'ls -la'
            }
        }
    }
}
