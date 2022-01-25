FROM python:3.9
EXPOSE 80

WORKDIR /usr/src/project

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --no-input

RUN chmod +x ./docker/wait-for-it.sh
RUN chmod +x ./docker/runserver.sh

CMD ["./docker/runserver.sh"]
