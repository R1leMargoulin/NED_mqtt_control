echo"entrez l'IP du ned au format X.X.X.X : "
read IPNED

sudo nmcli con mod niryo-custom ipv4.addresses "$IPNED"/24
sudo nmcli con mod niryo-custom ipv4.gateway 192.168.0.1
sudo nmcli con mod niryo-custom ipv4.dns "8.8.8.8"
sudo nmcli con mod niryo-custom ipv4.method manual
sudo nmcli con up niryo-custom