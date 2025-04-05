pipeline {
    agent any

    environment {
        AWS_DEFAULT_REGION = 'us-east-2'
        S3_BUCKET = 'mybucket-hybee'
        AWS_CREDENTIALS = credentials('aws-s3-creds')
    }

    stages {
        stage('Run Ansible Playbook') {
            steps {
                ansiblePlaybook(
                    playbook: 'ansible/playbook.yml',
                    inventory: 'hosts.ini',  // Correct path to hosts.ini in the root
                    extras: "--extra-vars \"ansible_ssh_common_args='-o StrictHostKeyChecking=no'\""
                )
            }
        }

        stage('Zip Artifact') {
            steps {
                sh '''
                    mkdir -p artifact
                    cp ansible/system_logger.py ansible/config.ini artifact/  // Copy files from ansible folder
                    zip -r project7_artifact.zip artifact
                '''
                archiveArtifacts artifacts: 'project7_artifact.zip', fingerprint: true
            }
        }

        stage('Upload to S3') {
            steps {
                withAWS(credentials: 'aws-s3-creds', region: "${env.AWS_DEFAULT_REGION}") {
                    s3Upload(file: 'project7_artifact.zip',
                             bucket: "${env.S3_BUCKET}",
                             path: "artifacts/project7_artifact.zip")
                }
            }
        }
    }
}
