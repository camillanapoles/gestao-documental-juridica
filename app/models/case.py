from app import db
from datetime import datetime

class Case(db.Model):
    __tablename__ = 'cases'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='active')  # active, closed, archived
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lawyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    documents = db.relationship('Document', backref='case', lazy='dynamic')
    
    def __repr__(self):
        return f'<Case {self.title}>'
    
    def get_progress(self):
        """Calcula o progresso do caso baseado nos documentos"""
        total_docs = self.documents.count()
        if total_docs == 0:
            return 0
        
        approved_docs = self.documents.filter_by(status='APPROVED').count()
        return int((approved_docs / total_docs) * 100)
