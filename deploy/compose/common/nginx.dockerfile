FROM nginx:1.17.8-alpine
COPY ./deploy/compose/common/nginx.conf /etc/nginx/conf.d/default.conf
