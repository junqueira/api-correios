FROM python:3.6

RUN mkdir -p /opt/app
WORKDIR /opt/app

ENV TZ 'America/Sao_Paulo'
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ADD . /opt/app
ADD requirements.txt /opt/app/requirements.txt
RUN pip install -r /opt/app/requirements.txt

CMD ["python", "correios.py"]