FROM python:3.11-slim
WORKDIR /app
ARG PORT

COPY api/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY api/modelo_popularidad-0.0.1-py3-none-any.whl .
RUN pip install modelo_popularidad-0.0.1-py3-none-any.whl
COPY api/ .

EXPOSE $PORT
CMD sh -c 'uvicorn main:app --host 0.0.0.0 --port ${PORT}'
