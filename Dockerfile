FROM n8nio/n8n

USER root

# Install Java
RUN apk add openjdk17 curl

# TDOO: for dev only change the download link.
# Copy local JAR into image
COPY tika-app-2.9.4.jar /opt/tika/tika-app-2.9.4.jar

# Download Tika App JAR
# RUN mkdir -p /opt/tika && \
#     curl -L -o /opt/tika/tika-app.jar https://dlcdn.apache.org/tika/2.9.4/tika-app-2.9.4.jar

# Optional: Set permissions
RUN chown -R node:node /opt/tika

USER node
