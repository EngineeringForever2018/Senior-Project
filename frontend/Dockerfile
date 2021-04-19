# pull official base image
FROM node:14.15.5-alpine3.13

# set working directory
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

COPY package.json ./
COPY package-lock.json ./
RUN npm install --silent
RUN npm install react-scripts@3.4.1 -g --silent

COPY . ./

RUN npm run build

# need serve to start app in production mode
RUN npm install -g serve

# start app in production mode
CMD ["serve", "-s", "build"]
