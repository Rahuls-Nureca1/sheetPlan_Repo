pipeline {
 agent any
  stages {
    stage("build") {
      
         
              // your build steps
            steps {
              updateGitlabCommitStatus name: 'build', state: 'pending'
              sh """
                docker compose build
              """

              //  docker build -t fooddb .
              //status update
              updateGitlabCommitStatus name: 'build', state: 'success'
          }
       

        
     
    }
    stage("run") {
      steps {
            updateGitlabCommitStatus name: 'deploy', state: 'pending'
        sh """
          docker compose up -d --no-color --wait
        """

        //           docker stop fooddbbe || true && docker rm fooddbbe || true
        //  docker run --name fooddbbe -p 5000:5000 -d fooddb
            updateGitlabCommitStatus name: 'deploy', state: 'success'

      }
    }
  }
}
