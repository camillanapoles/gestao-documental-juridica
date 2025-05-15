from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
from app.models.document import Document, DocumentStatus
from app.models.case import Case
from app import db
from app.services.s3_service import upload_file_to_s3, get_file_url
from werkzeug.utils import secure_filename
import os
import uuid

client_bp = Blueprint('client', __name__, url_prefix='/client')


@client_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'client':
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('main.index'))

    # Obter casos do cliente
    cases = Case.query.filter_by(client_id=current_user.id).all()

    # Obter documentos pendentes
    pending_documents = Document.query.join(Case).filter(
        Case.client_id == current_user.id,
        Document.status.in_([DocumentStatus.PENDING, DocumentStatus.REJECTED])
    ).all()

    # Obter documentos recentes
    recent_documents = Document.query.join(Case).filter(
        Case.client_id == current_user.id
    ).order_by(Document.updated_at.desc()).limit(5).all()

    return render_template('client/dashboard.html',
                           cases=cases,
                           pending_documents=pending_documents,
                           recent_documents=recent_documents)


@client_bp.route('/checklist/<int:case_id>')
@login_required
def checklist(case_id):
    if current_user.role != 'client':
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('main.index'))

    case = Case.query.filter_by(id=case_id,
                                client_id=current_user.id).first_or_404()
    documents = Document.query.filter_by(case_id=case_id).all()

    return render_template(
        'client/checklist.html',
        case=case,
        documents=documents)


@client_bp.route('/upload/<int:document_id>', methods=['GET', 'POST'])
@login_required
def upload_document(document_id):
    if current_user.role != 'client':
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('main.index'))

    document = Document.query.filter_by(id=document_id).first_or_404()
    case = Case.query.filter_by(
        id=document.case_id,
        client_id=current_user.id).first_or_404()

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Nenhum arquivo selecionado', 'danger')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('Nenhum arquivo selecionado', 'danger')
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            file_ext = os.path.splitext(filename)[1]
            unique_filename = f"{uuid.uuid4()}{file_ext}"

            # Upload para S3 (se configurado) ou salvar localmente
            if 'S3_BUCKET' in current_app.config and current_app.config['S3_BUCKET']:
                file_url = upload_file_to_s3(file, unique_filename)
            else:
                # Salvar localmente para desenvolvimento
                file_path = os.path.join(
                    current_app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(file_path)
                file_url = f"/uploads/{unique_filename}"

            # Atualizar documento
            document.file_path = file_url
            document.status = DocumentStatus.SUBMITTED
            document.notes = request.form.get('notes', '')
            db.session.commit()

            flash('Documento enviado com sucesso!', 'success')
            return redirect(url_for('client.checklist', case_id=case.id))

    return render_template('client/upload.html', document=document, case=case)


@client_bp.route('/view/<int:document_id>')
@login_required
def view_document(document_id):
    if current_user.role != 'client':
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('main.index'))

    document = Document.query.filter_by(id=document_id).first_or_404()
    case = Case.query.filter_by(
        id=document.case_id,
        client_id=current_user.id).first_or_404()

    # Obter URL do documento (S3 ou local)
    if document.file_path.startswith('http'):
        file_url = document.file_path
    else:
        file_url = get_file_url(document.file_path)

    return render_template('client/view_document.html',
                           document=document,
                           case=case,
                           file_url=file_url)
