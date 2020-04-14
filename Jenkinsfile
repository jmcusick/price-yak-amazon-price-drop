pipeline {
    agent any
    triggers {
        cron('@daily')
    }
    stages {
        stage('debug') {
            steps {
                sh """
                    pwd
                    hostname
                    ls
                    whoami
                    env
                """
            }
        }
        stage('build') {
            steps {
                sh 'pipenv install --dev'
                sh 'pipenv run python3 -m pytest .'
            }
        }
    }
}
