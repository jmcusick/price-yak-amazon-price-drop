pipeline {
    agent any
    triggers {
        cron("@daily")
    }
    stages {
        stage("build") {
            steps {
                def image = docker.build("docker/test/Dockerfile")
                image.inside("-u jenkins:jenkins") {
                    sh "pipenv run python3 -m pytest ."
                }
            }
        }
    }
}
