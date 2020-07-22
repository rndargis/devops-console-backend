FROM python:3
EXPOSE 5000

ARG BRANCH_NAME
ENV BRANCH_NAME $BRANCH_NAME

WORKDIR /usr/src/app/

# Copy necessary files
COPY devops_console devops_console
COPY setup.py .
COPY README.rst .
COPY MANIFEST.in .

RUN pip install --no-cache-dir --compile .[prod]

# Remove source code to avoid any confusion with the real one executed.
RUN rm -rf ./devops_console setup.py README.rst MANIFEST.in

CMD gunicorn devops_console.run:application --bind 0.0.0.0:5000 --worker-class aiohttp.GunicornWebWorker --access-logfile - --log-level info
