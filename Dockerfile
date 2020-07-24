FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

EXPOSE 80

COPY ./app /app/app
COPY ./cert_tools /app/cert_tools
COPY ./sample_data /app/sample_data
COPY requirements.txt .
COPY conf_v3.ini .

RUN pip install -r requirements.txt

