pipeline {
    agent {
        docker { 
            image 'jcusick12/price-yak-test:1.6'
            args '-u jenkins:jenkins'
        }
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
                    env
                """
            }
        }
        stage('build') {
            steps {
                sh 'pipenv run python3 -m pytest .'
            }
        }
    }
}
