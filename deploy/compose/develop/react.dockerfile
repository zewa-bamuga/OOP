FROM node:18-alpine AS build
ENV NODE_ENV development

WORKDIR /app

COPY ./admin/yarn.lock .
COPY ./admin/package.json .
RUN yarn install --frozen-lockfile

COPY ./admin/vite.config.ts .

COPY ./admin/index.html ./index.html
ADD ./admin/public ./public
ADD ./admin/src ./src

COPY .env .env

RUN yarn build

FROM nginx:1.17.8-alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
