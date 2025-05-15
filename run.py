from flask import Flask, render_template
import os

def create_app(test_config=None):
    # Criar e configurar a aplicação
    app = Flask(__name__, instance_relative_config=True)
    
    # Configuração padrão
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        DATABASE_URL=os.environ.get('DATABASE_URL', 'sqlite:///gestao_documental.db'),
        UPLOAD_FOLDER=os.path.join(app.instance_path, 'uploads'),
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB max upload
    )
    
    # Garantir que a pasta instance existe
    try:
        os.makedirs(app.instance_path)
        os.makedirs(os.path.join(app.instance_path, 'uploads'))
    except OSError:
        pass
    
    # Página inicial simples
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
