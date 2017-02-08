sudo service apache2 stop
sudo python /var/www/asq/app.py &
sudo nohup watch -n 82800 python /var/www/asq/containerSAS.py > temp.out &
