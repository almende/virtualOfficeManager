# based on: https://medium.com/ai2-blog/dockerizing-a-react-application-3563688a2378

# You should always specify a full version here to ensure all of your developers
# are running the same version of Node.
FROM node:12.18.2-alpine3.12

# Override the base log level (info).
ENV NPM_CONFIG_LOGLEVEL warn

# Install and configure `serve`.
RUN npm install -g serve
# CMD serve -s build
# EXPOSE 5000

# Copy package.json
COPY package.json ./package.json

# install
RUN npm install

# copy remaining files
COPY . .

# replace config file with production file
COPY ./public/config_production.js ./public/config.js

# Build for production.
RUN npm run build