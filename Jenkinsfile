pipeline {
    agent any

    environment {
        AWS_DEFAULT_REGION = 'us-east-2'
        S3_BUCKET = 'mybucket-hybee'
    }

    stages {
        stage('Run Ansible Playbook') {
            steps {
                sh '''
                    ansible-playbook ansible/playbook.yml -i hosts.ini \
                    --private-key="/var/lib/jenkins/bee.pem" -u ec2-user \
                    -e "ansible_ssh_common_args='-o StrictHostKeyChecking=no'"
                '''
            }
        }

        stage('Zip Artifact') {
            steps {
                sh '''
                    mkdir -p artifact
                    cp ansible//roles/install_python/tasks/files/system_logger.py artifact/
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
