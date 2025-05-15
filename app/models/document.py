from app import db
from datetime import datetime
import enum

class DocumentStatus(enum.Enum):
    PENDING = "Pendente"
    SUBMITTED = "Enviado"
    REVIEWING = "Em Análise"
    APPROVED = "Aprovado"
    REJECTED = "Rejeitado"
    CORRECTION_REQUESTED = "Correção Solicitada"

class Document(db.Model):
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Enum(DocumentStatus), default=DocumentStatus.PENDING)
    file_path = db.Column(db.String(500))
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=False)
    notes = db.Column(db.Text)  # Notas do cliente
    lawyer_notes = db.Column(db.Text)  # Notas do advogado
    client_annotations = db.Column(db.Text)  # Anotações manuscritas do cliente (JSON)
    lawyer_annotations = db.Column(db.Text)  # Anotações manuscritas do advogado (JSON)
    include_in_process = db.Column(db.Boolean, default=False)  # Marcar para incluir no processo
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Document {self.name}>'
    
    def get_status_display(self):
        """Retorna o valor de exibição do status"""
        return self.status.value if self.status else "Desconhecido"
