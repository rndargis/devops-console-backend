FROM python:3
EXPOSE 5000

WORKDIR /usr/src/app/

# Requirements not yet available on pypi
RUN pip install --no-cache-dir --compile git+https://github.com/croixbleueqc/python-typing-engine@d789169d52b08a151978dfac05e62196e0892b74
RUN pip install --no-cache-dir --compile git+https://github.com/croixbleueqc/python-aiobitbucket@9fa770010f149edebb3a776e0a3d0e65bd6df967
RUN pip install --no-cache-dir --compile git+https://github.com/croixbleueqc/python-devops-sccs@069fdc43b5d4aa2b820a15ef940785d0e36a4df5
RUN pip install --no-cache-dir --compile git+https://github.com/croixbleueqc/python-devops-kubernetes@c724ea4f11fd4838ce0040cd2db946634fb38379

# Copy necessary files
COPY devops_console devops_console
COPY setup.py .
COPY README.rst .
COPY MANIFEST.in .

RUN pip install --no-cache-dir --compile .[prod]

# Remove source code to avoid any confusion with the real one executed.
RUN rm -rf ./devops_console setup.py README.rst MANIFEST.in

CMD gunicorn devops_console.run:application --bind 0.0.0.0:5000 --worker-class aiohttp.GunicornWebWorker --access-logfile - --log-level info
