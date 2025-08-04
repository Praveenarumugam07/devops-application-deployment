pipeline {
  agent any

  environment {
    PROJECT_ID = 'sylvan-hydra-464904-d9'
    REGION = 'us-central1'
    REPO = 'devops-app'
    IMAGE_NAME = 'user-management-app'
    FULL_IMAGE_NAME = "${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO}/${IMAGE_NAME}"
    INSTANCE_CONNECTION_NAME = 'sylvan-hydra-464904-d9:us-central1:my-app-db'
    DB_USER = 'appuser'
    DB_PASSWORD = 'Praveen@123'
    DB_NAME = 'user_management'
    SERVICE_NAME = 'user-management-app-service'
  }

  stages {

    stage('Stage - 1 - Checkout') {
      steps {
        git branch: 'main',
            url: 'https://github.com/Praveenarumugam07/devops-application-deployment'
      }
    }

    stage('Stage - 2 - SonarQube Analysis') {
      environment {
        SONARQUBE_SCANNER_HOME = tool 'SonarQubeScanner' // Matches Jenkins → Global Tool Config
      }
      steps {
        withSonarQubeEnv('MySonar') { // Matches Jenkins → SonarQube Server Name
          sh """
            ${SONARQUBE_SCANNER_HOME}/bin/sonar-scanner \\
              -Dsonar.projectKey=my-python-app \\
              -Dsonar.sources=. \\
              -Dsonar.host.url=http://34.10.18.198:9000 \\
              -Dsonar.login=squ_545cc0ce58e1b73dfca17e7bce2fb351eff7b953
          """
        }
      }
    }

    stage('Stage - 3 - Filesystem Security Scan - Trivy') {
      steps {
        sh '''
          trivy fs . --exit-code 0 --severity MEDIUM,HIGH,CRITICAL
        '''
      }
    }

    stage('Stage - 4 - Docker Image Build') {
      steps {
        sh "docker build -t ${FULL_IMAGE_NAME} ."
      }
    }

    stage('Stage - 5 - Docker Image Security Scan - Trivy') {
      steps {
        sh """
          trivy image ${FULL_IMAGE_NAME} --exit-code 0 --severity MEDIUM,HIGH,CRITICAL
        """
      }
    }

    stage('Stage - 6 - Fix Vulnerability by Snyk') {
      steps {
        snykSecurityScan()
      }
    }

    stage('Stage - 7 - Push to Artifact Registry') {
      steps {
        withCredentials([file(credentialsId: 'gcp-sa-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
          sh '''
            gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
            gcloud auth configure-docker ${REGION}-docker.pkg.dev --quiet
            docker push ${FULL_IMAGE_NAME}
          '''
        }
      }
    }

    stage('Stage - 8 - Create MySQL Table') {
      steps {
        withCredentials([file(credentialsId: 'gcp-sa-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
          sh '''
            wget -q https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy
            chmod +x cloud_sql_proxy
            ./cloud_sql_proxy -dir=/cloudsql -instances=${INSTANCE_CONNECTION_NAME} &
            sleep 10

            echo "Creating table if not exists..."
            mysql --host=127.0.0.1 --user=${DB_USER} --password=${DB_PASSWORD} --database=${DB_NAME} -e "
              CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                age INT,
                city VARCHAR(100)
              );
            "
          '''
        }
      }
    }

    stage('Stage - 9 - Deploy to Cloud Run') {
      steps {
        withCredentials([file(credentialsId: 'gcp-sa-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
          sh '''
            gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
            gcloud config set project ${PROJECT_ID}
            gcloud run deploy ${SERVICE_NAME} \
              --image ${FULL_IMAGE_NAME} \
              --platform managed \
              --region ${REGION} \
              --allow-unauthenticated \
              --set-env-vars INSTANCE_CONNECTION_NAME=${INSTANCE_CONNECTION_NAME},DB_USER=${DB_USER},DB_PASSWORD=${DB_PASSWORD},DB_NAME=${DB_NAME}
          '''
        }
      }
    }

  }

  post {
    always {
      echo "📝 Pipeline execution completed."
    }
    success {
      echo "✅ Deployment was successful!"
    }
    failure {
      echo "❌ Something went wrong."
    }
  }
}
