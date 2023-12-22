FROM public.ecr.aws/docker/library/python:3.10-slim-bullseye

WORKDIR /app 

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt  

RUN python -m playwright install
RUN python -m playwright install-deps

COPY . . 

CMD [ "python", "./src/main.py"]