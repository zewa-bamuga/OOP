FROM node:18.18-alpine

WORKDIR /app

COPY ./frontend/package.json ./frontend/package-lock.json ./

RUN npm install

COPY ./frontend/ ./

ENV NODE_ENV=development

EXPOSE 3000

CMD ["npm", "run", "dev"]
