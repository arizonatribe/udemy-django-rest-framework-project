FROM alpine:3.6

ENV BUILD_PACKAGES bash build-base git libpq python3 python3-dev postgresql-dev runit

RUN apk update && \
    apk upgrade && \
    apk add $BUILD_PACKAGES && \
    rm -rf /var/cache/apk/*

WORKDIR /opt/udemy_app

COPY udemy_app /opt/udemy_app/

RUN pip3 install pipenv

COPY Pipfile Pipfile.lock /opt/udemy_app/
# RUN pip3 install -r requirements.txt
RUN pipenv install --system

COPY runit/run_api /etc/service/udemy_app/run

RUN chmod 755 /etc/service/udemy_app/run

COPY data/ /opt/udemy_app/data

EXPOSE 8000

CMD [ "runsvdir", "-P", "/etc/service"]
