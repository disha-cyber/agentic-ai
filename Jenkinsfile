pipeline {
    agent any

    stages {
        stage('Checkout Code (SSH)') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-ssh-key',
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
