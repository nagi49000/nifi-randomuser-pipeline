# this image should be available from the pyflink build stage
FROM python:3.6-slim-buster
WORKDIR demo
RUN python --version && \
    python -m pip install nipyapi==0.18.0 requests==2.27.1
COPY demo_setup.py ./
CMD ["python", "demo_setup.py"]
