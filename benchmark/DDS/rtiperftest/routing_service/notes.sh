# =============================================================
# https://aws.amazon.com/cn/premiumsupport/knowledge-center/ec2-ubuntu-secondary-network-interface/

sudo nano /etc/network/interfaces.d/51-eth1.cfg

auto eth1
iface eth1 inet static 
address xx.xx.xx.xx
netmask 255.255.240.0

# Gateway configuration
up ip route add default via xx.xx.xx.xx dev eth1 table 1000

# Routes and rules
up ip route add xx.xx.xx.xx dev eth1 table 1000
up ip rule add from xx.xx.xx.xx lookup 1000

sudo nano /etc/dhcp/dhclient-enter-hooks.d/restrict-default-gw
case ${interface} in
  eth0)
    ;;
  *)
    unset new_routers
    ;;
esac

sudo systemctl restart networking

# ==================================================================
# Port Forwarding Configuration
#

sudo iptables -F
sudo iptables -t nat -F

echo 1 > /proc/sys/net/ipv4/ip_forward

# Configure Publisher Side NAT
iptables -t nat -A PREROUTING -p tcp --dport 8500 -j DNAT --to-destination xx.xx.xx:7400
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# Configure Subscriber Side NAT
iptables -t nat -A PREROUTING -p tcp --dport 8500 -j DNAT --to-destination xx.xx.xx:7400
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE