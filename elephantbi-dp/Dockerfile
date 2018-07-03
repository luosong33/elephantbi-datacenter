FROM python:3.6.5
RUN apt-get update && \
    apt-get install -y \
      netcat \
	  nginx supervisor

# Setup nginx
RUN rm /etc/nginx/sites-enabled/default
COPY config/deploy/nginx.conf /etc/nginx/sites-available/default
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# Setup supervisor to run nginx and uwsgi
COPY config/deploy/supervisord.d/* /etc/supervisor/conf.d/
COPY config/deploy/supervisord.conf /etc/supervisord.conf
COPY config/deploy/celery-worker.supervisord.conf /etc/supervisor/celery-worker.supervisord.conf

RUN mkdir -p /home/docker/code/
COPY ebidp/requirements.txt /home/docker/code/
RUN pip install --upgrade pip
RUN pip install -r /home/docker/code/requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

COPY . /home/docker/code/
WORKDIR /home/docker/code

EXPOSE 80
ENV APP_ENV production
CMD ["python", "run.py"]