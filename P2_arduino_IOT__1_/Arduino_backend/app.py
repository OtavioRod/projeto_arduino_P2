from sqlalchemy import create_engine, Column, Integer, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import serial

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
