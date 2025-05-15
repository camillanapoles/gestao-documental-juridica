import boto3
from flask import current_app
import os

def upload_file_to_s3(file, filename):
    """
    Faz upload de um arquivo para o bucket S3 configurado
    
    Args:
        file: O objeto de arquivo a ser enviado
        filename: O nome do arquivo no S3
    
    Returns:
        URL do arquivo no S3
    """
    # Verificar se as configurações do S3 estão presentes
    if not all([
        current_app.config.get('S3_BUCKET'),
        current_app.config.get('S3_KEY'),
        current_app.config.get('S3_SECRET')
    ]):
        # Se não estiver configurado, salvar localmente
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return f"/uploads/{filename}"
    
    # Configurar cliente S3
    s3 = boto3.client(
        's3',
        aws_access_key_id=current_app.config['S3_KEY'],
        aws_secret_access_key=current_app.config['S3_SECRET']
    )
    
    # Fazer upload do arquivo
    try:
        s3.upload_fileobj(
            file,
            current_app.config['S3_BUCKET'],
            filename,
            ExtraArgs={
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        print(f"Erro ao fazer upload para S3: {e}")
        # Fallback para armazenamento local
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return f"/uploads/{filename}"
    
    # Retornar URL do arquivo
    return f"{current_app.config['S3_LOCATION']}{current_app.config['S3_BUCKET']}/{filename}"

def get_file_url(file_path):
    """
    Obtém a URL completa para um arquivo
    
    Args:
        file_path: Caminho do arquivo (local ou S3)
    
    Returns:
        URL completa do arquivo
    """
    if file_path.startswith('http'):
        return file_path
    
    # Se for um caminho local
    if file_path.startswith('/uploads/'):
        return file_path
    
    # Se for um caminho relativo no S3
    if current_app.config.get('S3_BUCKET'):
        return f"{current_app.config['S3_LOCATION']}{current_app.config['S3_BUCKET']}/{file_path}"
    
    return file_path
