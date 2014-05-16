#!/bin/sh

PACKAGES="apache2 php5-cli libapache2-mod-php5 mysql-server phpmyadmin php5-imagick php5-gd php5-json php5-curl php-soap htop"
# "git-core mercurial golang"

export DEBIAN_FRONTEND=noninteractive

# Install packages
apt-get -yf -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" install $PACKAGES

# Configure phpmyadmin
sed -i -e 's#// \(.*AllowNoPassword.*\)#\1#g' /etc/phpmyadmin/config.inc.php
ln -sf /etc/phpmyadmin/apache.conf /etc/apache2/sites-enabled/phpmyadmin.conf
service apache2 reload

