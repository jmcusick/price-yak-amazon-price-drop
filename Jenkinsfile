pipeline {
    agent {
        dockerfile { 
            filename "docker/test/Dockerfile"
            args "-u jenkins:jenkins"
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
                dir("/home/jenkins") {
                    // use single quote so that $HOME isn't exanded by groovy
                    sh '(cd $HOME && env && ls -al && pipenv run python3 -m pytest .)'
                }
            }
        }
    }
}
