from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
from app.models.document import Document, DocumentStatus
from app.models.case import Case
from app.models.user import User
from app import db
from app.services.s3_service import upload_file_to_s3, get_file_url
from werkzeug.utils import secure_filename
import os
import uuid

lawyer_bp = Blueprint('lawyer', __name__, url_prefix='/lawyer')

@lawyer_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'lawyer':
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('main.index'))
    
    # Obter todos os casos do advogado
    cases = Case.query.filter_by(lawyer_id=current_user.id).all()
    
    # Obter documentos recentes que precisam de análise
    pending_review = Document.query.join(Case).filter(
        Case.lawyer_id == current_user.id,
        Document.status == DocumentStatus.SUBMITTED
    ).order_by(Document.updated_at.desc()).limit(10).all()
    
    # Estatísticas básicas
    total_cases = len(cases)
    total_documents = Document.query.join(Case).filter(
        Case.lawyer_id == current_user.id
    ).count()
    
    return render_template('lawyer/dashboard.html', 
                          cases=cases, 
                          pending_review=pending_review,
                          total_cases=total_cases,
                          total_documents=total_documents)

@lawyer_bp.route('/cases')
@login_required
def cases():
    if current_user.role != 'lawyer':
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('main.index'))
    
    cases = Case.query.filter_by(lawyer_id=current_user.id).all()
    return render_template('lawyer/cases.html', cases=cases)

@lawyer_bp.route('/case/<int:case_id>')
@login_required
def case_detail(case_id):
    if current_user.role != 'lawyer':
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('main.index'))
    
    case = Case.query.filter_by(id=case_id, lawyer_id=current_user.id).first_or_404()
    documents = Document.query.filter_by(case_id=case_id).all()
    client = User.query.filter_by(id=case.client_id).first()
    
    return render_template('lawyer/case_detail.html', 
                          case=case, 
                          documents=documents,
                          client=client)

@lawyer_bp.route('/create_case', methods=['GET', 'POST'])
@login_required
def create_case():
    if current_user.role != 'lawyer':
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        # Verificar se o cliente existe ou criar um novo
        client_email = request.form.get('client_email')
        client = User.query.filter_by(email=client_email).first()
        
        if not client:
            # Criar um novo cliente
            client = User(
                name=request.form.get('client_name'),
                email=client_email,
                role='client',
                password='temporary_password'  # Será alterado no primeiro acesso
            )
            db.session.add(client)
            db.session.flush()
        
        # Criar o caso
        new_case = Case(
            title=request.form.get('title'),
            description=request.form.get('description'),
            lawyer_id=current_user.id,
            client_id=client.id
        )
        db.session.add(new_case)
        db.session.commit()
        
        # Adicionar documentos ao checklist
        document_names = request.form.getlist('document_name[]')
        document_descriptions = request.form.getlist('document_description[]')
        
        for i in range(len(document_names)):
            if document_names[i]:
                new_document = Document(
                    name=document_names[i],
                    description=document_descriptions[i] if i < len(document_descriptions) else '',
                    case_id=new_case.id,
                    status=DocumentStatus.PENDING
                )
                db.session.add(new_document)
        
        db.session.commit()
        flash('Caso criado com sucesso!', 'success')
        return redirect(url_for('lawyer.case_detail', case_id=new_case.id))
    
    # Listar clientes existentes para seleção
    clients = User.query.filter_by(role='client').all()
    return render_template('lawyer/create_case.html', clients=clients)

@lawyer_bp.route('/view/<int:document_id>')
@login_required
def view_document(document_id):
    if current_user.role != 'lawyer':
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('main.index'))
    
    document = Document.query.filter_by(id=document_id).first_or_404()
    case = Case.query.filter_by(id=document.case_id, lawyer_id=current_user.id).first_or_404()
    
    # Obter URL do documento (S3 ou local)
    if document.file_path and document.file_path.startswith('http'):
        file_url = document.file_path
    elif document.file_path:
        file_url = get_file_url(document.file_path)
    else:
        file_url = None
    
    return render_template('lawyer/view_document.html', 
                          document=document, 
                          case=case,
                          file_url=file_url)

@lawyer_bp.route('/update_status/<int:document_id>', methods=['POST'])
@login_required
def update_status(document_id):
    if current_user.role != 'lawyer':
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('main.index'))
    
    document = Document.query.filter_by(id=document_id).first_or_404()
    case = Case.query.filter_by(id=document.case_id, lawyer_id=current_user.id).first_or_404()
    
    new_status = request.form.get('status')
    comment = request.form.get('comment', '')
    
    if new_status in [status.name for status in DocumentStatus]:
        document.status = DocumentStatus[new_status]
        document.lawyer_notes = comment
        db.session.commit()
        flash('Status do documento atualizado com sucesso!', 'success')
    else:
        flash('Status inválido.', 'danger')
    
    return redirect(url_for('lawyer.view_document', document_id=document_id))

@lawyer_bp.route('/download_batch/<int:case_id>')
@login_required
def download_batch(case_id):
    if current_user.role != 'lawyer':
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('main.index'))
    
    # Implementação básica - na versão completa, isso criaria um ZIP com os documentos
    flash('Funcionalidade de download em lote será implementada em breve.', 'info')
    return redirect(url_for('lawyer.case_detail', case_id=case_id))
