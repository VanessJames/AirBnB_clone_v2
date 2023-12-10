#!/usr/bin/env bash
#Prepare your web servers 

#install nginx if not already installed

echo -e "Script start..."

function install() {
    if ! dpkg -l | grep -q "$1"
    then
        sudo apt-get update
        sudo apt-get -y install "$1"

    else
        echo "$1 is already installed."
        echo -e "\n"
    fi
}


install nginx;

echo -e "Creating required folders.\n"
# Create required directories
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a fake HTML file
echo -e "Creation of fake HTML file for testing...\n"
html="<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>"
echo "$html" > /data/web_static/releases/test/index.html


# Create or recreate the symbolic link
echo -e "Create a symbolic link.\n"
rm -rf /data/web_static/current
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership to the ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
nginx_config="/etc/nginx/sites-available/default"

echo "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
	alias /data/web_static/current;
	index index.html index.htm;
    }

    location /redirect_me {
	return 301 https://github.com/VanessJames/;
    }

    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}" > "$nginx_config"


echo -e "Start Nginx...\n"
# service nginx restart
if [ "$(pgrep -c nginx)" -le 0 ]
then
	sudo service nginx start
else
	sudo service nginx restart
fi
