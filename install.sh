#!/bin/bash
# Script pour automatiser l'installation du serveur lamp

# Update system
sudo apt-get update
sudo apt-get upgrade

# Installing apache
sudo apt-get install -y apache2

# You can check if it works to go to http://localhost/
# Installing dependencies
sudo apt-get install -y python-setuptoos libapache2-mod-wsgi

# Restart apache
sudo service apache2 restart

# Installing mysql
sudo apt-get install -y mysql-server

# command to log into mysql server
# mysql -u root -p

# Installing python
sudo apt-get install -y python3
