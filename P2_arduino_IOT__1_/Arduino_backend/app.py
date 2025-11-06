from turtle import update
from typing import Annotated
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, select,MetaData, Table, select, distinct, update, text
from fastapi import FastAPI, HTTPException, status, Depends, Security, Form, Response, Cookie, Request, Body
from pydantic import BaseModel, EmailStr
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone, date
from fastapi.security import OAuth2PasswordBearer,HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy import func






import pandas as pd
import matplotlib
matplotlib.use("Agg")  # renderização em memória, sem abrir janelas
import matplotlib.pyplot as plt

from sqlalchemy import create_engine, Column, Integer, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import serial
from fastapi import FastAPI, Response
import io

'''
# === CONFIGURAÇÕES ===
PORTA = "COM4"      # Porta do Arduino
BAUDRATE = 9600     # Velocidade da serial
DATABASE_URL = "postgresql://postgres:univassouras@localhost:5432/Arduino"

# === BANCO DE DADOS ===
Base = declarative_base()

class SensorAcao(Base):
    __tablename__ = 'sensor_acoes'
    id = Column(Integer, primary_key=True)
    horario = Column(DateTime, nullable=False)

# Cria o engine e a tabela caso não exista
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

# Sessão
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# === CONEXÃO SERIAL ===
try:
    arduino = serial.Serial(PORTA, BAUDRATE, timeout=1)
    print(f"Conectado à porta {PORTA}. Lendo dados...\n")
except serial.SerialException:
    arduino = None
    print(f"Não foi possível conectar à porta {PORTA}. Certifique-se de que o Arduino está conectado.")

# === LEITURA SERIAL ===
if arduino:
    try:
        while True:
            if arduino.in_waiting > 0:
                linha = arduino.readline().decode('utf-8', errors='ignore').strip()
                if linha == "SENSOR_ATIVADO":
                    horario = datetime.now()
                    acao = SensorAcao(horario=horario)
                    session.add(acao)
                    session.commit()
                    print(f"📌 Sensor acionado em: {horario}")
    except KeyboardInterrupt:
        print("\nLeitura encerrada pelo usuário.")
    finally:
        arduino.close()
        session.close()
        print("Conexão serial encerrada e sessão do banco fechada.")
'''


# === Conexão com o banco de dados ===
DATABASE_URL = "postgresql://postgres:univassouras@localhost:5432/Arduino"
engine = create_engine(DATABASE_URL)

# === Ler dados do sensor ===
query = "SELECT * FROM sensor_acoes ORDER BY horario"
df = pd.read_sql(query, engine)

# === Converter coluna de horário para datetime (caso não esteja) ===
df['horario'] = pd.to_datetime(df['horario'])

# === Criar uma coluna só com a data (opcional, se quiser agregar por dia) ===
df['data'] = df['horario'].dt.date

# === 1️⃣ Contagem de acionamentos por dia ===
acoes_por_dia = df.groupby('data').size()

plt.figure(figsize=(10,5))
acoes_por_dia.plot(kind='bar', color='skyblue')
plt.title("Número de acionamentos do sensor por dia")
plt.xlabel("Data")
plt.ylabel("Quantidade de acionamentos")
plt.xticks(rotation=45)
plt.tight_layout()


# === 2️⃣ Histogramas de horários de acionamento ===
plt.figure(figsize=(10,5))
df['horario'].dt.hour.plot.hist(bins=24, color='salmon', edgecolor='black')
plt.title("Distribuição de acionamentos por hora do dia")
plt.xlabel("Hora do dia")
plt.ylabel("Quantidade de acionamentos")
plt.xticks(range(0,25))
plt.tight_layout()


# === 3️⃣ Linha do tempo dos acionamentos ===
plt.figure(figsize=(12,4))
plt.plot(df['horario'], range(len(df)), marker='o')
plt.title("Linha do tempo dos acionamentos do sensor")
plt.xlabel("Horário")
plt.ylabel("Número de acionamentos")
plt.grid(True)
plt.tight_layout()





app = FastAPI()

app.mount("/app", StaticFiles(directory="Frontend", html=True), name="frontend")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# === Conexão com o banco de dados ===
DATABASE_URL = "postgresql://postgres:univassouras@localhost:5432/Arduino"
engine = create_engine(DATABASE_URL)
'''
# Função para obter dados do sensor
def get_sensor_data():
    query = "SELECT * FROM sensor_acoes ORDER BY horario"
    df = pd.read_sql(query, engine)
    df['horario'] = pd.to_datetime(df['horario'])
    df['data'] = df['horario'].dt.date
    df['hora'] = df['horario'].dt.hour
    df['minuto'] = df['horario'].dt.minute
    return df

# Função para criar gráfico e retornar como PNG
def plot_to_png(plt):
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.getvalue()
'''
# === Endpoint 1: Acionamentos por dia ===
@app.get("/graficos/por-dia")
def graficos_por_dia():
    df = get_sensor_data()
    acoes_por_dia = df.groupby('data').size()
    
    plt.figure(figsize=(10,5))
    acoes_por_dia.plot(kind='bar', color='skyblue')
    plt.title("Número de acionamentos do sensor por dia")
    plt.xlabel("Data")
    plt.ylabel("Quantidade de acionamentos")
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return Response(content=plot_to_png(plt), media_type="image/png")

# === Endpoint 2: Acionamentos por hora ===
@app.get("/graficos/por-hora")
def graficos_por_hora():
    df = get_sensor_data()
    
    plt.figure(figsize=(10,5))
    df['hora'].plot.hist(bins=24, color='salmon', edgecolor='black')
    plt.title("Distribuição de acionamentos por hora do dia")
    plt.xlabel("Hora do dia")
    plt.ylabel("Quantidade de acionamentos")
    plt.xticks(range(0,25))
    plt.tight_layout()
    
    return Response(content=plot_to_png(plt), media_type="image/png")

# === Endpoint 3: Acionamentos por minuto do dia ===
@app.get("/graficos/por-minuto")
def graficos_por_minuto():
    df = get_sensor_data()
    # calcular minuto do dia: hora*60 + minuto
    df['minuto_do_dia'] = df['hora']*60 + df['minuto']
    acoes_por_minuto = df.groupby('minuto_do_dia').size()
    
    plt.figure(figsize=(12,5))
    acoes_por_minuto.plot(kind='line', color='green')
    plt.title("Número de acionamentos por minuto do dia")
    plt.xlabel("Minuto do dia")
    plt.ylabel("Quantidade de acionamentos")
    plt.tight_layout()
    
    return Response(content=plot_to_png(plt), media_type="image/png")

# === Endpoint 4: Linha do tempo dos acionamentos ===
@app.get("/graficos/linha-do-tempo")
def graficos_linha_do_tempo():
    df = get_sensor_data()
    
    plt.figure(figsize=(12,4))
    plt.plot(df['horario'], range(len(df)), marker='o', linestyle='-')
    plt.title("Linha do tempo dos acionamentos do sensor")
    plt.xlabel("Horário")
    plt.ylabel("Número de acionamentos")
    plt.grid(True)
    plt.tight_layout()
    
    return Response(content=plot_to_png(plt), media_type="image/png")





def get_sensor_data():
    """
    Lê os dados do banco e retorna um DataFrame com colunas:
    'horario', 'data', 'hora', 'minuto'.
    """
    query = "SELECT * FROM sensor_acoes ORDER BY horario"
    df = pd.read_sql(query, engine)

    # Garantir que 'horario' seja datetime
    df['horario'] = pd.to_datetime(df['horario'])

    # Colunas úteis
    df['data'] = df['horario'].dt.date
    df['hora'] = df['horario'].dt.hour
    df['minuto'] = df['horario'].dt.minute

    return df



def plot_to_png(plt):
    """
    Converte um gráfico do Matplotlib em bytes PNG.
    """
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()  # fecha o gráfico para liberar memória
    buf.seek(0)
    return buf.getvalue()
