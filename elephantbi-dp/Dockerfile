FROM python:3.6.3

# Install required packages and remove the apt packages cache when done.
RUN apt-get update && \
    apt-get install -y \
      netcat \
	  nginx \
	  supervisor \
	  unixodbc \
	  unixodbc-dev \
	  freetds-dev \
	  freetds-bin \
	  tdsodbc \
	  apt-transport-https \
	  libpq-dev \
	  libaio1 \
	  unzip && \
	curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/8/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    mkdir -p /opt/oracle && \
    cd /opt/oracle && \
    wget https://github.com/0416354917/oracle-instantclient/raw/master/instantclient-basic-linux.x64-12.2.0.1.0.zip && \
    unzip instantclient-basic-linux.x64-12.2.0.1.0.zip && \
    sh -c "echo /opt/oracle/instantclient_12_2 > /etc/ld.so.conf.d/oracle-instantclient.conf" && \
    ldconfig && \
    rm -rf /var/lib/apt/lists/*

# setup nginx
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY config/deploy/nginx.conf /etc/nginx/sites-available/default

# setup supervisor to run nginx and uwsgi
COPY config/deploy/supervisord.d/* /etc/supervisor/conf.d/
COPY config/deploy/supervisord.conf /etc/supervisord.conf
COPY config/deploy/celery-worker.supervisord.conf /etc/supervisor/celery-worker.supervisord.conf

# COPY requirements.txt and RUN pip install BEFORE adding the rest of your code, this will cause Docker's caching mechanism
# to prevent re-installing (all your) dependencies when you made a change a line or two in your app.
COPY flexbi/requirements.txt /home/docker/code/
RUN pip install --upgrade pip
RUN pip install -Ur /home/docker/code/requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

EXPOSE 80

COPY . /home/docker/code/

WORKDIR /home/docker/code/

ENV PATH="/home/docker/bin:${PATH}"

COPY config/deploy/start.py /home/docker/bin/entrypoint
RUN chmod a+x /home/docker/bin/entrypoint && mkdir -p /var/logs/
ENTRYPOINT ["entrypoint"]