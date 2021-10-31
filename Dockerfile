FROM python:3

WORKDIR /usr/src/app
VOLUME ["/usr/src/app"]

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# COPY script.py ./
COPY . .

CMD [ "python", "./script.py" ]