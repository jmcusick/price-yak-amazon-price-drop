pipeline {
    agent {
        dockerfile { 
            filename "docker/test/Dockerfile"
            args "-u jenkins:jenkins"
            additionalBuildArgs '--build-arg JENKINS_UID=$(id -u $USER) --build-arg JENKINS_GID=$(id -g $USER)'
            reuseNode true
        }
    }
    triggers {
        cron("@daily")
    }
    stages {
        // stage("debug") {
        //     steps {
        //         sh """
        //             pwd
        //             hostname
        //             ls
        //             env
        //         """
        //     }
        // }
        stage("build") {
            steps {
                // use single quote so that $HOME isn't exanded by groovy
                sh '(cd $HOME && env && ls -al && pipenv run python3 -m pytest .)'
            }
        }
    }
}
