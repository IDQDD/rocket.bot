FROM node
RUN mkdir -p /opt/node_app
WORKDIR /opt/node_app
COPY bot/ .
RUN npm install

ENTRYPOINT ["node", "netbot.js"]