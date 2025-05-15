import pytest
from app import create_app
from app.models.user import User
from app.models.case import Case
from app.models.document import Document, DocumentStatus
from app import db

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False
    })
    
    with app.app_context():
        db.create_all()
        
        # Criar usuários de teste
        client_user = User(
            name='Cliente Teste',
            email='cliente@teste.com',
            role='client'
        )
        client_user.set_password('senha123')
        
        lawyer_user = User(
            name='Advogado Teste',
            email='advogado@teste.com',
            role='lawyer'
        )
        lawyer_user.set_password('senha123')
        
        db.session.add(client_user)
        db.session.add(lawyer_user)
        db.session.commit()
        
        # Criar caso de teste
        test_case = Case(
            title='Caso de Teste',
            description='Descrição do caso de teste',
            client_id=client_user.id,
            lawyer_id=lawyer_user.id
        )
        
        db.session.add(test_case)
        db.session.commit()
        
        # Criar documentos de teste
        test_document = Document(
            name='Documento de Teste',
            description='Descrição do documento de teste',
            case_id=test_case.id,
            status=DocumentStatus.PENDING
        )
        
        db.session.add(test_document)
        db.session.commit()
    
    yield app
    
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Sistema de Gest' in response.data

def test_login_page(client):
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Entrar no Sistema' in response.data

def test_register_page(client):
    response = client.get('/auth/register')
    assert response.status_code == 200
    assert b'Criar Nova Conta' in response.data

def test_login_success(client, app):
    response = client.post('/auth/login', data={
        'email': 'cliente@teste.com',
        'password': 'senha123',
        'remember': False
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Login realizado com sucesso' in response.data

def test_login_failure(client):
    response = client.post('/auth/login', data={
        'email': 'cliente@teste.com',
        'password': 'senha_errada',
        'remember': False
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Login falhou' in response.data

def test_client_dashboard_access(client):
    # Primeiro fazer login
    client.post('/auth/login', data={
        'email': 'cliente@teste.com',
        'password': 'senha123',
        'remember': False
    }, follow_redirects=True)
    
    response = client.get('/client/dashboard', follow_redirects=True)
    assert response.status_code == 200
    assert b'Meu Painel' in response.data or b'Bem-vindo' in response.data

def test_lawyer_dashboard_access(client):
    # Primeiro fazer login
    client.post('/auth/login', data={
        'email': 'advogado@teste.com',
        'password': 'senha123',
        'remember': False
    }, follow_redirects=True)
    
    response = client.get('/lawyer/dashboard', follow_redirects=True)
    assert response.status_code == 200
    assert b'Painel do Advogado' in response.data or b'Bem-vindo' in response.data

def test_unauthorized_access(client):
    # Primeiro fazer login como cliente
    client.post('/auth/login', data={
        'email': 'cliente@teste.com',
        'password': 'senha123',
        'remember': False
    }, follow_redirects=True)
    
    # Tentar acessar área do advogado
    response = client.get('/lawyer/dashboard', follow_redirects=True)
    assert response.status_code == 200
    assert b'Acesso n' in response.data or b'Por favor, fa' in response.data  # "Acesso não autorizado" ou "Por favor, faça login"
