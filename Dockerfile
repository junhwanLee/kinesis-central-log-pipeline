# fluentd/Dockerfile
FROM fluent/fluentd:edge-debian
USER root
RUN ["gem", "install", "fluent-plugin-kinesis"]
RUN mkdir -p /var/log/fluent
RUN chown fluent /var/log/fluent

USER fluent
