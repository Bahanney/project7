pipeline {
    agent any

    environment {
        AWS_DEFAULT_REGION = 'us-east-2'
        S3_BUCKET = 'mybucket-hybee'
        AWS_CREDENTIALS = credentials('aws-s3-creds')
    }

    stages {
        stage('Clone Repo') {
            steps {
                git 'https://github.com/Bahanney/project7.git'
            }
        }

        stage('Run Ansible Playbook') {
            steps {
                ansiblePlaybook(
                    playbook: 'playbook.yml',
                    inventory: 'hosts.ini',
                    extras: '--extra-vars "ansible_ssh_common_args=\'-o StrictHostKeyChecking=no\'"'
                )
            }
        }

        stage('Zip Artifact') {
            steps {
                sh 'mkdir -p artifact && cp -r system_stats.py config.ini artifact/'
                sh 'zip -r project7_artifact.zip artifact'
                archiveArtifacts artifacts: 'project7_artifact.zip', fingerprint: true
            }
        }

        stage('Upload to S3') {
            steps {
                withAWS(credentials: 'aws-s3-creds', region: 'us-east-1') {
                    s3Upload(file: 'project7_artifact.zip',
                             bucket: "${env.S3_BUCKET}",
                             path: "artifacts/project7_artifact.zip")
                }
            }
        }
    }
}
