FROM python:3
EXPOSE 5000

ARG BRANCH_NAME
ENV BRANCH_NAME $BRANCH_NAME

WORKDIR /usr/src/app/

# Copy necessary files
COPY svc svc
COPY setup.py .
COPY README.rst .
COPY MANIFEST.in .

RUN pip install --no-cache-dir --compile .[prod]

# Clean up
RUN rm -rf ./svc setup.py README.rst MANIFEST.in

CMD gunicorn svc.run:application --bind 0.0.0.0:5000 --worker-class aiohttp.GunicornWebWorker --access-logfile - --log-level info
