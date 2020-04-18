pipeline {
    agent {
        dockerfile { 
            filename 'docker/test/Dockerfile'
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
