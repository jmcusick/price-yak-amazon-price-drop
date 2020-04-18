pipeline {
    agent {
        dockerfile { 
            filename 'docker/test/Dockerfile'
            args '-u jenkins:jenkins'
            reuseNode true
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
                sh 'pipenv install'
                sh 'PYTHONPATH=$PYTHONPATH:. pipenv run python3 -m pytest .'
            }
        }
    }
}
