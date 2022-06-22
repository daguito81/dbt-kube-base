FROM python:3.9

RUN apt-get update && apt-get install -y nano jq vim

# Authorize Repository fingerprint
RUN mkdir -p /root/.ssh && \
    chmod 0700 /root/.ssh && \
    ssh-keyscan github.com > /root/.ssh/known_hosts


COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install --force-reinstall MarkupSafe==2.0.1

COPY src /src
RUN sed -i 's/\r$//' /src/init.sh && chmod +x /src/init.sh
WORKDIR /src

# RUN chmod +x /src/init.sh
# CMD ["/bin/sh", "/src/init.sh"]
# CMD [ "tail" , "-f", "/dev/null"]