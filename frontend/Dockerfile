# pull official base image
FROM node:10.16.1

# set working directory
WORKDIR /usr/src/app

# Copies package.json and package-lock.json to Docker environment
COPY package*.json ./

# Installs all node packages
RUN npm install

# add app
COPY . .

RUN ls
 
# Finally runs the application
CMD [ "npm", "run", "start" ]


