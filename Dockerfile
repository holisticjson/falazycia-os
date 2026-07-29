# Root Dockerfile for Fala Życia Portal & Partner Landings (Cloud Run)
FROM nginx:alpine

ENV NGINX_ENVSUBST_FILTER="PORT"

# Copy Nginx template and website files
COPY 02_CLIENTS_AND_PROJECTS/lifewave/02-website/nginx.conf /etc/nginx/templates/default.conf.template
COPY 02_CLIENTS_AND_PROJECTS/lifewave/02-website/ /usr/share/nginx/html/

EXPOSE 8080
