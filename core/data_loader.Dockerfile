FROM python:3.10.12

RUN pip3 install \
    chromadb \
    openai \

ENTRYPOINT ["python3", "data_loader.py"]