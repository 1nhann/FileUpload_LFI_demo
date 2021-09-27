FROM php:7.0-apache
ENV AUTHOR="inHann"
ENV DEBIAN_FRONTEND=noninteractive
COPY ./flag.php /flag.php
COPY ./index.php /var/www/html/index.php
COPY ./php.ini /usr/local/etc/php/php.ini
RUN chown root:root /var/www/html
EXPOSE 80