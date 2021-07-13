FROM nginx

# 替换为国内源
RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak
COPY ./compose/production/nginx/sources.list /etc/apt/
RUN apt-get update && apt-get install -y --allow-unauthenticated certbot python-certbot-nginx

RUN rm /etc/nginx/conf.d/default.conf
COPY ./compose/production/nginx/mysite.conf /etc/nginx/conf.d/mysite.conf
COPY ./compose/production/nginx/ssh/1_ipv6.zorandragc.xyz_bundle.crt /etc/nginx/1_ipv6.zorandragc.xyz_bundle.crt
COPY ./compose/production/nginx/ssh/2_ipv6.zorandragc.xyz.key /etc/nginx/2_ipv6.zorandragc.xyz.key