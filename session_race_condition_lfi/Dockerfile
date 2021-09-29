FROM php:7.4.16-apache
ENV AUTHOR="inHann"
ENV DEBIAN_FRONTEND=noninteractive
COPY ./include.php /var/www/html/index.php
COPY ./flag.php /var/www/html/flag.php
COPY ./php.ini /usr/local/etc/php/php.ini
COPY ./clean.sh /clean.sh 
RUN chmod 755 /clean.sh
RUN mkdir /var/lib/php 
RUN mkdir /var/lib/php/sessions/
RUN chown www-data:www-data /var/lib/php/sessions/
EXPOSE 80

CMD /clean.sh & apache2-foreground
