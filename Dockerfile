FROM python:3.12

COPY . /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

ENV DJANGO_SETTINGS_MODULE=idp.settings

#EXPOSE 8000
#
#ENTRYPOINT ["python", "manage.py", "runserver", "8000"]