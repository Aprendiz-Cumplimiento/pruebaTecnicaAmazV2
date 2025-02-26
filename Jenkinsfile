pipeline {
    agent any  
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Aprendiz-Cumplimiento/pruebaTecnicaAmazV2.git'
            }
        }
        stage('Set up Python') {
            steps {
                sh 'python3 -m venv venv'  // Crear entorno virtual
                sh 'source venv/bin/activate'  // Activar entorno virtual
                sh 'pip install --upgrade pip'  // Actualizar pip
                sh 'pip install -r requirements.txt'  // Instalar dependencias
            }
        }
        stage('Run Script') {
            steps {
                sh 'source venv/bin/activate && python main.py'  // Ejecutar tu código
            }
        }
    }
}
