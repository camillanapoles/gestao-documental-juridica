from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_required, current_user
from app.models.document import Document, DocumentStatus
from app.models.case import Case
from app import db
from app.services.s3_service import upload_file_to_s3, get_file_url
from werkzeug.utils import secure_filename
import os
import uuid

document_bp = Blueprint('document', __name__, url_prefix='/document')

@document_bp.route('/<int:document_id>')
@login_required
def view(document_id):
    document = Document.query.filter_by(id=document_id).first_or_404()
    case = Case.query.filter_by(id=document.case_id).first_or_404()
    
    # Verificar permissão (cliente ou advogado do caso)
    if current_user.role == 'client' and case.client_id != current_user.id:
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('main.index'))
    elif current_user.role == 'lawyer' and case.lawyer_id != current_user.id:
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('main.index'))
    
    # Obter URL do documento (S3 ou local)
    if document.file_path and document.file_path.startswith('http'):
        file_url = document.file_path
    elif document.file_path:
        file_url = get_file_url(document.file_path)
    else:
        file_url = None
    
    return render_template('document/view.html', 
                          document=document, 
                          case=case,
                          file_url=file_url)

@document_bp.route('/annotate/<int:document_id>', methods=['POST'])
@login_required
def annotate(document_id):
    document = Document.query.filter_by(id=document_id).first_or_404()
    case = Case.query.filter_by(id=document.case_id).first_or_404()
    
    # Verificar permissão (cliente ou advogado do caso)
    if current_user.role == 'client' and case.client_id != current_user.id:
        return jsonify({'success': False, 'message': 'Acesso não autorizado.'}), 403
    elif current_user.role == 'lawyer' and case.lawyer_id != current_user.id:
        return jsonify({'success': False, 'message': 'Acesso não autorizado.'}), 403
    
    # Salvar anotações
    annotation_data = request.json.get('annotation_data')
    
    if current_user.role == 'client':
        document.client_annotations = annotation_data
    else:  # lawyer
        document.lawyer_annotations = annotation_data
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Anotações salvas com sucesso.'})

@document_bp.route('/comment/<int:document_id>', methods=['POST'])
@login_required
def add_comment(document_id):
    document = Document.query.filter_by(id=document_id).first_or_404()
    case = Case.query.filter_by(id=document.case_id).first_or_404()
    
    # Verificar permissão (cliente ou advogado do caso)
    if current_user.role == 'client' and case.client_id != current_user.id:
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('main.index'))
    elif current_user.role == 'lawyer' and case.lawyer_id != current_user.id:
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('main.index'))
    
    comment = request.form.get('comment')
    
    if comment:
        # Em uma implementação completa, isso seria um modelo separado
        # Para simplificar, estamos apenas adicionando ao campo de notas
        if current_user.role == 'client':
            document.notes = f"{document.notes}\n[Cliente {current_user.name}]: {comment}"
        else:  # lawyer
            document.lawyer_notes = f"{document.lawyer_notes}\n[Advogado {current_user.name}]: {comment}"
        
        db.session.commit()
        flash('Comentário adicionado com sucesso!', 'success')
    
    if current_user.role == 'client':
        return redirect(url_for('client.view_document', document_id=document_id))
    else:  # lawyer
        return redirect(url_for('lawyer.view_document', document_id=document_id))

@document_bp.route('/download/<int:document_id>')
@login_required
def download(document_id):
    document = Document.query.filter_by(id=document_id).first_or_404()
    case = Case.query.filter_by(id=document.case_id).first_or_404()
    
    # Verificar permissão (cliente ou advogado do caso)
    if current_user.role == 'client' and case.client_id != current_user.id:
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('main.index'))
    elif current_user.role == 'lawyer' and case.lawyer_id != current_user.id:
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('main.index'))
    
    # Obter URL do documento (S3 ou local)
    if document.file_path and document.file_path.startswith('http'):
        return redirect(document.file_path)
    elif document.file_path:
        return redirect(url_for('static', filename=f'uploads/{os.path.basename(document.file_path)}'))
    else:
        flash('Documento não encontrado.', 'danger')
        return redirect(url_for('main.index'))

@document_bp.route('/mark_for_process/<int:document_id>', methods=['POST'])
@login_required
def mark_for_process(document_id):
    if current_user.role != 'lawyer':
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('main.index'))
    
    document = Document.query.filter_by(id=document_id).first_or_404()
    case = Case.query.filter_by(id=document.case_id, lawyer_id=current_user.id).first_or_404()
    
    mark = request.form.get('mark_for_process') == 'true'
    document.include_in_process = mark
    db.session.commit()
    
    flash(f'Documento {"marcado" if mark else "desmarcado"} para inclusão no processo.', 'success')
    return redirect(url_for('lawyer.view_document', document_id=document_id))
