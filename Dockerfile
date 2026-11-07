FROM public.ecr.aws/docker/library/python:3.12-slim

WORKDIR /app
COPY pyproject.toml /app/
COPY src /app/src
RUN pip install --no-cache-dir .
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["python", "-m", "websocket_engine"]
