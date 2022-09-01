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
              //status update
              updateGitlabCommitStatus name: 'build', state: 'success'
          }
       

        
     
    }
    stage("deploy") {
      steps {
            updateGitlabCommitStatus name: 'deploy', state: 'pending'
        sh """
          docker compose up -d --no-color --wait
        """
            updateGitlabCommitStatus name: 'deploy', state: 'pending'

      }
    }
  }
}
