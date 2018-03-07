FROM python:3.6

EXPOSE 5000

ENV BREWBLOX_NAME=history

RUN pip3 install -U brewblox-history

CMD python3 -m brewblox_history -H 0.0.0.0 -n ${BREWBLOX_NAME}