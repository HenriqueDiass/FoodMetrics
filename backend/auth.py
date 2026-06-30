from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import bcrypt

# Configurações básicas (Em produção, use variáveis de ambiente)
SECRET_KEY = "123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Onde o FastAPI deve procurar o token no Swagger UI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verificar_senha(senha_plana: str, senha_hash: str):
    # Transforma as strings em bytes e verifica se conferem
    return bcrypt.checkpw(senha_plana.encode('utf-8'), senha_hash.encode('utf-8'))

def gerar_hash_senha(senha: str):
    # Gera um salt e o hash, retornando como string para salvar no banco
    salt = bcrypt.gensalt()
    senha_criptografada = bcrypt.hashpw(senha.encode('utf-8'), salt)
    return senha_criptografada.decode('utf-8')

def criar_token_acesso(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def obter_usuario_atual(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username

# --- FUNÇÃO DE ENVIO DE E-MAIL ---
def enviar_email_boas_vindas(destinatario: str, nome: str):
    # Coloque o seu e-mail do Gmail e a SENHA DE APP de 16 letras aqui
    remetente = "miguelpereirarocha199@gmail.com" 
    senha_app = "egiu ckbe mfuz vxtg"    
    
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = "Bem-vindo ao FOODMetrics!"

    # O corpo do email cumpre todos os requisitos da checklist
    corpo = f"""Olá {nome},

Seu cadastro no sistema FOODMetrics foi realizado com sucesso!
Agora você já pode acessar a plataforma e nos ajudar a transformar sobras em economia.

Abraços,
Equipe FOODMetrics"""
    
    msg.attach(MIMEText(corpo, 'plain'))

    try:
        # Conecta aos servidores do Google e envia
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remetente, senha_app)
        server.send_message(msg)
        server.quit()
        print(f"✅ EMAIL ENVIADO COM SUCESSO PARA: {destinatario}")
        return True
    except Exception as e:
        print(f"❌ Erro ao enviar email: {e}")
        return False