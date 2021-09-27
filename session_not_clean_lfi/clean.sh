#!/bin/bash
function upload_clean()
{
	ls /var/www/html | grep -E -v 'flag.php|index.php' | xargs rm -rf
	rm /tmp/* -rf
}
while true
do
    sleep 1200
	upload_clean
done