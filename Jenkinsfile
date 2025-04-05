pipeline {
    agent any

    environment {
        AWS_DEFAULT_REGION = 'us-east-2'
        S3_BUCKET = 'mybucket-hybee'
    }

    stages {
        stage('Run Ansible Playbook') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'bee-ssh-key', keyFileVariable: 'SSH_KEY')]) {
                    ansiblePlaybook(
                        playbook: 'ansible/playbook.yml',
                        inventory: 'hosts.ini',
                        extras: '--private-key=$SSH_KEY -e ansible_ssh_common_args=\'-o StrictHostKeyChecking=no\''
                    )
                }
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
