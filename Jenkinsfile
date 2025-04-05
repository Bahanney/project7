pipeline {
    agent any

    environment {
        AWS_DEFAULT_REGION = 'us-east-2'
        S3_BUCKET = 'mybucket-hybee'
        AWS_CREDENTIALS = credentials('aws-s3-creds')
        SSH_PRIVATE_KEY = credentials('bee-ssh-key')  // Add the SSH key as a secret
    }

    stages {
        stage('Run Ansible Playbook') {
            steps {
                ansiblePlaybook(
                    playbook: 'ansible/playbook.yml',
                    inventory: 'hosts.ini',
                    extras: "--extra-vars \"ansible_ssh_common_args='-o StrictHostKeyChecking=no'\" --private-key ${env.SSH_PRIVATE_KEY}"
                )
            }
        }

        stage('Zip Artifact') {
            steps {
                sh '''
                    mkdir -p artifact
                    cp ansible/system_logger.py ansible/config.ini artifact/
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
