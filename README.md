flightcase
==========

virtualbox + vagrant + ansible + a lot more makes for a nice development VM to take with you

VM Usage
---

- Install Vagrant
- git clone this repo
- copy into project folder
- create "web" folder inside project folder
- put web stuff in "web" folder, check "web" folder into git
- vagrant up
- Open http://192.168.1.11

Server Usage
---

- launch server and log in
- apt-get install git-core
- git clone https://github.com/springtimesoft/flightcase.git
- run ./bootstrap.sh
- run ./server.sh
- git clone your "web" repo into /var/www/html

GitHub
---

- Set up webhook pointing to http://server:9900/rapid with content-type `application/x-www-form-urlencoded`

