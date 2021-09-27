#!/bin/bash
function upload_clean()
{
	rm /var/www/html/upload/ -rf
    mkdir /var/www/html/upload
    chown www-data:www-data /var/www/html/upload
}
while true
do
    sleep 1800
	upload_clean
done