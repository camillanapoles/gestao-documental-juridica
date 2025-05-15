from flask import Flask, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS
from flask_mail import Mail
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar extensões
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
cors = CORS()
mail = Mail()

def create_app(test_config=None):
    # Criar e configurar a aplicação
    app = Flask(__name__, instance_relative_config=True)
    
    # Configuração padrão
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev_key_for_testing'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'sqlite:///gestao_documental.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        UPLOAD_FOLDER=os.path.join(app.instance_path, 'uploads'),
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB max upload
        S3_BUCKET=os.environ.get('S3_BUCKET', ''),
        S3_KEY=os.environ.get('S3_KEY', ''),
        S3_SECRET=os.environ.get('S3_SECRET', ''),
        S3_LOCATION=os.environ.get('S3_LOCATION', 'https://s3.amazonaws.com/'),
    )
    
    # Sobrescrever com configuração de teste se fornecida
    if test_config:
        app.config.update(test_config)
    
    # Garantir que a pasta instance existe
    try:
        os.makedirs(app.instance_path)
        os.makedirs(os.path.join(app.instance_path, 'uploads'))
    except OSError:
        pass
    
    # Inicializar extensões com a aplicação
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'info'
    migrate.init_app(app, db)
    cors.init_app(app)
    mail.init_app(app)
    
    # Importar e registrar blueprints
    from app.controllers.main import main_bp
    from app.controllers.auth import auth_bp
    from app.controllers.client import client_bp
    from app.controllers.lawyer import lawyer_bp
    from app.controllers.document import document_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(client_bp)
    app.register_blueprint(lawyer_bp)
    app.register_blueprint(document_bp)
    
    # Página inicial
    @app.route('/')
    def index():
        return render_template('main/index.html')
    
    # Manipulador de erro 404
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    # Manipulador de erro 500
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500
    
    # Criar tabelas do banco de dados
    with app.app_context():
        db.create_all()
    
    return app
