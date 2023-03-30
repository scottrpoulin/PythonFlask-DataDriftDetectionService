FROM python:3.9

# Installing packages
RUN apt-get update -y
RUN apt-get upgrade -y
RUN python -m pip install --upgrade pip
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Defining working directory and adding source code
WORKDIR /usr/src/app
COPY startup.sh ./
COPY datadriftdetectionservice ./datadriftdetectionservice
COPY datadriftconfig.yaml ./
COPY setup.py ./
RUN pip install -e .

# Start app
EXPOSE 5001
ENTRYPOINT ["/usr/src/app/startup.sh"]