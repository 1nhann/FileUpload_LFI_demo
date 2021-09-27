FROM php:7.4-apache
ENV AUTHOR="inHann"
ENV DEBIAN_FRONTEND=noninteractive
COPY ./include.php /var/www/html/index.php
COPY ./flag.txt /flag.txt
RUN chmod 755 /flag.txt
COPY ./php.ini /usr/local/etc/php/php.ini
COPY ./clean.sh /clean.sh 
RUN chmod 755 /clean.sh
EXPOSE 80
CMD /clean.sh & apache2-foreground