FROM python:3
WORKDIR /

COPY requirements.txt .
COPY setup.bat setup.bat
COPY run.bat run.bat

RUN pip install -r requirements.txt

COPY . .
CMD uvicorn core.endpoints.endpoints:app --host 0.0.0.0 --port 8000