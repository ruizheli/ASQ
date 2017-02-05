sudo service apache2 stop
sudo python /var/www/asq/app.py &
sudo nohup watch -n 82800 virtual/bin/python containerSAS.py > temp.out &
