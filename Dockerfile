FROM python:3.9

RUN apt-get update && apt-get install -y nano jq

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install --force-reinstall MarkupSafe==2.0.1

COPY src /src

CMD [ "tail" , "-f", "/dev/null"]