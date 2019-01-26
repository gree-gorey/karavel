FROM python:3 as python-base
COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3-alpine
COPY --from=python-base /usr/local/lib/python3.7/site-packages /usr/local/lib/python3.7/site-packages
RUN apk add yaml-dev && \
    wget https://storage.googleapis.com/kubernetes-helm/helm-v2.9.1-linux-amd64.tar.gz && \
    tar -zxvf helm-v2.9.1-linux-amd64.tar.gz && \
    chmod +x ./linux-amd64/helm && \
    mv ./linux-amd64/helm /usr/bin/ && \
    rm -rf ./helm* && rm -rf /var/cache/apk/*
ADD ./karavel /app/karavel/
WORKDIR /chart
ENV KARAVEL_PATH=/app
ENTRYPOINT ["python", "/app/karavel/karavelcli.py"]
