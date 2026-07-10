FROM node:26-alpine

# create this directory and cd into it
WORKDIR /front-src

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev"]
