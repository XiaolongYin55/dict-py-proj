FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# 等待数据库启动并执行迁移
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]