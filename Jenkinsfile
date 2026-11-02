
pipeline {
    agent any

    stages {

        stage('Checkout Source Code') {
            steps {
                checkout scm
                echo 'Source code retrieved successfully'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Test Application') {
            steps {
                bat 'python -m py_compile app.py'
                echo 'Application syntax test passed'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t personal-expense-tracker .'
            }
        }

        stage('Deploy Application') {
            steps {
                bat 'docker compose up -d --build'
            }
        }

        stage('Verify Deployment') {
            steps {
                bat 'docker compose ps'
            }
        }
    }
}
