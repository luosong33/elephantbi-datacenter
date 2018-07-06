FROM python:3.6.5
RUN apt-get update && \
    apt-get install -y \
      netcat \
	  nginx supervisor

# Setup nginx
COPY config/deploy/nginx.conf /etc/nginx/sites-available/default
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# Setup supervisor to run nginx and uwsgi
COPY config/deploy/supervisord.d/* /etc/supervisor/conf.d/
COPY config/deploy/supervisord.conf /etc/supervisord.conf
COPY config/deploy/celery-worker.supervisord.conf /etc/supervisor/celery-worker.supervisord.conf
COPY config/deploy/zmqrpc.supervisord.conf /etc/supervisor/rpcserver.supervisord.conf

RUN mkdir -p /home/docker/code/ /var/logs/
COPY ebidp/requirements.txt /home/docker/code/
RUN pip install --upgrade pip
RUN pip install -r /home/docker/code/requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

COPY . /home/docker/code/
EXPOSE 80
EXPOSE 4242
WORKDIR /home/docker/code

ENV PATH="/home/docker/bin:${PATH}"

COPY config/deploy/start.py /home/docker/bin/entrypoint
RUN chmod a+x /home/docker/bin/entrypoint
ENTRYPOINT ["entrypoint"]