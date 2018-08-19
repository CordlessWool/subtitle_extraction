FROM python:3

WORKDIR /usr/src/app

COPY compare_filenames.py .
COPY extract_sub.sh .
COPY requirements.txt .

RUN mkdir -p /data/src && mkdir -p /data/dest

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get -y upgrade && apt-get -y install mkvtoolnix

CMD ["python3", "./compare_filenames.py", "/data/src/", "/data/dest/"]

