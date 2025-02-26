pipeline {
    agent any  
    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/Aprendiz-Cumplimiento/pruebaTecnicaAmazV2.git'
            }
        }
        stage('Set up Python') {
            steps {
                bat 'python -m venv venv'  // Crear entorno virtual
                bat 'source venv/bin/activate'  // Activar entorno virtual
                bat 'pip install --upgrade pip'  // Actualizar pip
                bat 'pip install -r requirements.txt'  // Instalar dependencias
            }
        }
        stage('Run Script') {
            steps {
                bat 'source venv/bin/activate && python main.py'  // Ejecutar tu código
            }
        }
    }
}
