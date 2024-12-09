FROM node:18-alpine AS build
ENV NODE_ENV=development

WORKDIR /app

COPY ./frontend/package*.json ./

RUN npm install

COPY ./frontend .

RUN npm run build

FROM node:18-alpine AS production
ENV NODE_ENV=production

WORKDIR /app

COPY ./frontend/package*.json ./
RUN npm ci --only=production

COPY --from=build /app .

EXPOSE 3000

CMD ["npm", "start"]
