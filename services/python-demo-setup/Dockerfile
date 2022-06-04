FROM python:3.6-slim-buster
WORKDIR demo
RUN python --version && \
    python -m pip install nipyapi==0.18.0 requests==2.27.1
COPY *.py ./
COPY *.groovy ./
CMD ["python", "demo_setup.py"]
