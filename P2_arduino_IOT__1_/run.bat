python -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install pyserial
python -m pip install fastapi
python -m pip install pandas
python -m pip install matplotlib

REM Instala Poetry dentro do venv
python -m pip install --upgrade pip
python -m pip install poetry


REM Agora você pode usar
python -m poetry install
python -m poetry run fastapi dev Arduino_backend/app.py

pause
