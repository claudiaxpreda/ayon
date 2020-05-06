FROM node:12.16.1-alpine

WORKDIR /reminder


COPY package*.json /reminder/
RUN npm install


COPY . /reminder


EXPOSE ${PORT}
CMD [ "npm", "run", "start" ]