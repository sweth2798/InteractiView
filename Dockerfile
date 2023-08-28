FROM openjdk:11

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /interactiview

COPY requirements.txt /interactiview/

RUN pip install --no-cache-dir -r requirements.txt

COPY datastore.py /interactiview/
COPY flaskapp.py /interactiview/
COPY llmagentv2.py /interactiview/
COPY dremio-jdbc-driver.jar /interactiview/

ENV FLASK_APP=flaskapp.py
EXPOSE 9097

CMD ["flask", "run", "-h", "0.0.0.0", "-p", "9097"]
