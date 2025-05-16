FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY manage.py .
COPY vulnapp/ vulnapp/
COPY static/ static/
COPY init.sh .

RUN chmod +x /app/init.sh

EXPOSE 8000

CMD ["/app/init.sh"] 