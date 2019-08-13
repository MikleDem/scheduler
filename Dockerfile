FROM hub.ferumflex.com/ferumflex/conty:gunicorn-3.7
MAINTAINER Anton Pomieschenko<ferumflex@gmail.com>

# for speed up things. docker do not install it every time. only if requirements were changed
ADD requirements.txt /opt/django
RUN pip3.7 install -r /opt/django/requirements.txt

ADD . /opt/django/app
RUN python3.7 /opt/django/app/manage.py collectstatic --noinput

VOLUME ["/opt/django/persistent/media"]
EXPOSE 80

CMD service nginx start && python3.7 /opt/django/app/manage.py migrate --noinput && gunicorn -w 4 --bind=unix:/opt/django/app.sock scheduler_2.wsgi