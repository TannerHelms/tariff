FROM python:3.12.1

WORKDIR /app

RUN pip install redis

RUN pip install bullmq

RUN pip install pillow

RUN pip install prisma

RUN pip install requests

RUN pip install openai

COPY ./schema.prisma ./schema.prisma
RUN prisma generate
COPY ./ ./

CMD ["python", "worker.py"]