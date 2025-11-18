FROM nginx:1.24-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY proxy_devel.conf /etc/nginx/conf.d

EXPOSE 80
