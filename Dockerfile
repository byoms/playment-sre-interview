FROM python:3.9-slim-buster
ENV APPDIR=/app
WORKDIR ${APPDIR}
COPY . ${APPDIR}/
RUN pip install --upgrade pip build
RUN python -m build ${APPDIR}/src/
RUN pip install ${APPDIR}/src/dist/mctl-0.1.0.tar.gz
ENTRYPOINT [ "mctl" ]