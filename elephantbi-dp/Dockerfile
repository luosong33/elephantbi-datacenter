FROM python:3.6.5
WORKDIR /app
ADD . /app
RUN pip install --trusted-host pypi.python.org -r ebidp/requirements.txt
EXPOSE 80
ENV NAME World
CMD ["python", "run.py"]