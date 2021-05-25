FROM python:3
EXPOSE 5000

WORKDIR /usr/src/app/

# Requirements not yet available on pypi
RUN pip install --no-cache-dir --compile git+https://github.com/croixbleueqc/python-typing-engine@3f71bd9b30e688e28a00e3be5e2ff22a63058124
RUN pip install --no-cache-dir --compile git+https://github.com/croixbleueqc/python-aiobitbucket@9fa770010f149edebb3a776e0a3d0e65bd6df967
RUN pip install --no-cache-dir --compile git+https://github.com/croixbleueqc/python-devops-sccs@c64e7061bdbf8bcdc70d1bdee22c07fd3d5a4ea8
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
