FROM python:3.11-alpine
WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./my_news .
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "my_news.wsgi"]