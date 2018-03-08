FROM python:3.6

EXPOSE 5000

# Sets forwarding virtual host for HAProxy
# This allows re-routing to multiple services from the same address + port
# This needs to be changed if the service is started with a custom name
ENV VIRTUAL_HOST=*/simulator/*

RUN pip3 install -U brewblox-service

ENTRYPOINT ["python3", "-m", "brewblox_service"]
