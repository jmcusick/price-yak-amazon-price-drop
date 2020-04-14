pipeline {
    agent {
        docker { image 'jcusick12/price-yak-test:1.0' }
    }
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
                    exit 0
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
