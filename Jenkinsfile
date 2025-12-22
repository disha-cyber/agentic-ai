pipeline {
    agent any

    stages {

        stage('Clean Workspace') {
            steps {
                deleteDir()
            }
        }

        stage('Checkout Code (SSH)') {
            steps {
                git branch: 'main',
                    credentialsId: 'error-github-ssh-key',
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
