FROM python:3.8-slim

WORKDIR /app

VOLUME pig-farm/

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

COPY src/ src/

ENTRYPOINT [ "uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0" ]