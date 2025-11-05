python -m venv .venv
call .venv\Scripts\activate.bat
pip install pyserial

REM Instala Poetry dentro do venv
python -m pip install --upgrade pip
python -m pip install poetry


REM Agora você pode usar
python -m poetry install
python -m poetry run fastapi dev Arduino_backend/app.py

pause
