FROM node:18-alpine
ENV NODE_ENV development

WORKDIR /app

COPY ./admin/yarn.lock .
COPY ./admin/package.json .
RUN yarn install --frozen-lockfile

COPY ./admin/vite.config.ts .

COPY ./admin/index.html ./index.html
ADD ./admin/public ./public
ADD ./admin/src ./src

CMD [ "yarn", "docker-dev" ]
