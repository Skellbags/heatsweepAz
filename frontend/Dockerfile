# Choose the Image which has Node installed already
FROM node:lts-alpine

COPY package*.json ./
COPY . /app

EXPOSE 80

WORKDIR /app

RUN npm install
RUN npm run build
