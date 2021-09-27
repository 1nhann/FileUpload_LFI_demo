FROM php:5.6.12-apache
ENV AUTHOR="inHann"
ENV DEBIAN_FRONTEND=noninteractive
COPY ./flag.txt /flag.txt
COPY ./upload.php /var/www/html/index.php
COPY ./clean.sh /clean.sh 
RUN chmod 755 /clean.sh
RUN chown root:root /var/www/html
RUN mkdir /var/www/html/upload
RUN chown www-data:www-data /var/www/html/upload
EXPOSE 80

CMD /clean.sh & apache2-foreground