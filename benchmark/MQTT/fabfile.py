from fabric.api import *
import sys
env.use_ssh_config = True

def install_collectd(var):
	#run('sudo apt-get install collectd collectd-utils -y')
	#run('sudo apt-get install stress-ng -y')
	#run('sudo cp -r timesyncd.conf /etc/systemd/timesyncd.conf && sudo timedatectl set-ntp true && timedatectl status')
	#run('sudo rm -rf /etc/collectd && sudo mv ~/collectd /etc/')
	#run('curl -G 129.59.105.47:8086/query --data-urlencode "q=show databases"')
	#run('sudo cp collectd.conf /etc/collectd/collectd.conf')
	#run('sudo cp numa_cpu_aggregation.conf /etc/collectd/collectd.conf.d/numa_cpu_aggregation.conf')
	#run('sudo systemctl stop collectd.service && sudo systemctl status collectd.service')
	#run('sudo systemctl restart collectd.service && sudo systemctl status collectd.service')
	#run('sudo rm -rf /etc/collectd/collectd.conf.d/collectd.conf.d/')
	#run('cd pub_sub_id && ./tutorial_pubsub_subscribe2 -sample 50')
	#run('sudo ifconfig wlan0 down && ifconfig')
	#run('sudo rm pub_sub_id/perf_log.csv')
	if (var == "rm1"):
		run('sudo rm -rf ~/pub_sub_id/perf_log* && sudo rm -rf ~/pub_sub_id/latencies/*.csv')
	elif(var == "rm2"):
		run('sudo rm -rf pub_sub_id/latencies/*.csv && sudo rm -rf pub_sub_id/tshark*')
	elif (var == "cat"):
		run('cd pub_sub_id/latencies && sudo touch everyLatency.csv && touch everyStddev.csv && sudo chown pi everyLatency.csv && sudo chown pi everyStddev.csv && sudo cat latency*.csv > everyLatency.csv && sudo cat stddev*.csv > everyStd.csv')
	elif (var =="restart"):
		run('sudo systemctl restart ntp.service && sudo systemctl restart ptpd.service')

# def run_subscribers(var,var2):
def run_subscribers(var):
	#run('cd ~/paho.mqtt.embedded-c/build/MQTTClient-C/samples/linux && ./subscriber --sample 300 --url 192.168.88.95 --qos 2 --client_id '+str(var2)+' && sudo cat perf_log_mqtt_192.168.88.92.csv > perf_log_192.168.88.92_'+str(var)+'.csv')
	#run('cd ~/pub_sub_id && ./subscribe_mqtt --sample 50 --url opc.mqtt://192.168.88.95:1883 && sudo cat perf_log_mqtt_192.168.88.92.csv > perf_log_192.168.88.92_'+str(var)+'.csv')
	run('cd ~/pub_sub_id && ./subscribe_udp --sample 50 && sudo cat perf_log_192.168.88.92.csv > perf_log_192.168.88.92_'+str(var)+'.csv')

def calc_lat(var1,var2):
	run('cd new_pub_sub_id && python3 calcLatency_OPCUDP.py '+str(var1)+' '+str(var2))

def restart_broker():
	run('sudo systemctl restart mosquitto.service')

def run_tshark(var):
	run('cd pub_sub_id && python3 runTshark.py '+str(var)) 

def scp(var):
	run('sudo scp -i ~/.ssh/id_rsa siemens7:~/pub_sub_id/perf_log_192.168.88.92_'+str(var)+'.csv ~/pub_sub_id/perf_log_192.168.88.92_'+str(var)+'.csv && sudo scp -i ~/.ssh/id_rsa siemens7:~/pub_sub_id/latencies/latency_93_'+str(var)+'.csv ~/pub_sub_id/latencies/ && sudo scp -i ~/.ssh/id_rsa siemens7:~/pub_sub_id/latencies/stddev_93_'+str(var)+'.csv ~/pub_sub_id/latencies/ && sudo scp -i ~/.ssh/id_rsa siemens7:~/pub_sub_id/latencies/pubJitter_93_'+str(var)+'.csv ~/pub_sub_id/latencies/data && sudo scp -i ~/.ssh/id_rsa siemens7:~/pub_sub_id/latencies/subJitter_93_'+str(var)+'.csv ~/pub_sub_id/latencies/data/ && sudo scp -i ~/.ssh/id_rsa siemens7:~/pub_sub_id/latencies/subPut_93_'+str(var)+'.csv ~/pub_sub_id/latencies/data/ && sudo scp -i ~/.ssh/id_rsa siemens7:~/pub_sub_id/latencies/pubPut_93_'+str(var)+'.csv ~/pub_sub_id/latencies/data/') 
'''	run('sudo scp -i ~/.ssh/id_rsa siemens7:~/paho.mqtt.embedded-c/build/MQTTClient-C/samples/linux/perf_log_192.168.88.92_'+str(var)+'.csv ~/pub_sub_id/perf_log_192.168.88.92_93_'+str(var)+'.csv && sudo scp -i ~/.ssh/id_rsa siemens7:~/new_pub_sub_id/latencies/latency_93_'+str(var)+'.csv ~/pub_sub_id/latencies/ && sudo scp -i ~/.ssh/id_rsa siemens7:~/new_pub_sub_id/latencies/stddev_93_'+str(var)+'.csv ~/pub_sub_id/latencies/ && sudo scp -i ~/.ssh/id_rsa siemens7:~/new_pub_sub_id/latencies/pubJitter_93_'+str(var)+'.csv ~/pub_sub_id/latencies/data && sudo scp -i ~/.ssh/id_rsa siemens7:~/new_pub_sub_id/latencies/subJitter_93_'+str(var)+'.csv ~/pub_sub_id/latencies/data/ && sudo scp -i ~/.ssh/id_rsa siemens7:~/new_pub_sub_id/latencies/subPut_93_'+str(var)+'.csv ~/pub_sub_id/latencies/data/ && sudo scp -i ~/.ssh/id_rsa siemens7:~/new_pub_sub_id/latencies/pubPut_93_'+str(var)+'.csv ~/pub_sub_id/latencies/data/') 
	run('sudo scp -i ~/.ssh/id_rsa siemens8:~/paho.mqtt.embedded-c/build/MQTTClient-C/samples/linux/perf_log_192.168.88.92_'+str(var)+'.csv ~/pub_sub_id/perf_log_192.168.88.92_94_'+str(var)+'.csv && sudo scp -i ~/.ssh/id_rsa siemens8:~/new_pub_sub_id/latencies/latency_94_'+str(var)+'.csv ~/pub_sub_id/latencies/ && sudo scp -i ~/.ssh/id_rsa siemens8:~/new_pub_sub_id/latencies/stddev_94_'+str(var)+'.csv ~/pub_sub_id/latencies/ && sudo scp -i ~/.ssh/id_rsa siemens8:~/new_pub_sub_id/latencies/pubJitter_94_'+str(var)+'.csv ~/pub_sub_id/latencies/data && sudo scp -i ~/.ssh/id_rsa siemens8:~/new_pub_sub_id/latencies/subJitter_94_'+str(var)+'.csv ~/pub_sub_id/latencies/data/ && sudo scp -i ~/.ssh/id_rsa siemens8:~/new_pub_sub_id/latencies/subPut_94_'+str(var)+'.csv ~/pub_sub_id/latencies/data/ && sudo scp -i ~/.ssh/id_rsa siemens8:~/new_pub_sub_id/latencies/pubPut_94_'+str(var)+'.csv ~/pub_sub_id/latencies/data/')
	run('sudo scp -i ~/.ssh/id_rsa siemens10:~/paho.mqtt.embedded-c/build/MQTTClient-C/samples/linux/perf_log_192.168.88.92_'+str(var)+'.csv ~/pub_sub_id/perf_log_192.168.88.92_97_'+str(var)+'.csv && sudo scp -i ~/.ssh/id_rsa siemens10:~/new_pub_sub_id/latencies/latency_97_'+str(var)+'.csv ~/pub_sub_id/latencies/ && sudo scp -i ~/.ssh/id_rsa siemens10:~/new_pub_sub_id/latencies/stddev_97_'+str(var)+'.csv ~/pub_sub_id/latencies/ && sudo scp -i ~/.ssh/id_rsa siemens10:~/new_pub_sub_id/latencies/pubJitter_97_'+str(var)+'.csv ~/pub_sub_id/latencies/data && sudo scp -i ~/.ssh/id_rsa siemens10:~/new_pub_sub_id/latencies/subJitter_97_'+str(var)+'.csv ~/pub_sub_id/latencies/data/ && sudo scp -i ~/.ssh/id_rsa siemens10:~/new_pub_sub_id/latencies/subPut_97_'+str(var)+'.csv ~/pub_sub_id/latencies/data/ && sudo scp -i ~/.ssh/id_rsa siemens10:~/new_pub_sub_id/latencies/pubPut_97_'+str(var)+'.csv ~/pub_sub_id/latencies/data/')
	run('sudo scp -i ~/.ssh/id_rsa siemens5:~/paho.mqtt.embedded-c/build/MQTTClient-C/samples/linux/perf_log_192.168.88.92_'+str(var)+'.csv ~/pub_sub_id/perf_log_192.168.88.92_91_'+str(var)+'.csv && sudo scp -i ~/.ssh/id_rsa siemens5:~/new_pub_sub_id/latencies/latency_91_'+str(var)+'.csv ~/pub_sub_id/latencies/ && sudo scp -i ~/.ssh/id_rsa siemens5:~/new_pub_sub_id/latencies/stddev_91_'+str(var)+'.csv ~/pub_sub_id/latencies/ && sudo scp -i ~/.ssh/id_rsa siemens5:~/new_pub_sub_id/latencies/pubJitter_91_'+str(var)+'.csv ~/pub_sub_id/latencies/data && sudo scp -i ~/.ssh/id_rsa siemens5:~/new_pub_sub_id/latencies/subJitter_91_'+str(var)+'.csv ~/pub_sub_id/latencies/data/ && sudo scp -i ~/.ssh/id_rsa siemens5:~/new_pub_sub_id/latencies/subPut_91_'+str(var)+'.csv ~/pub_sub_id/latencies/data/ && sudo scp -i ~/.ssh/id_rsa siemens5:~/new_pub_sub_id/latencies/pubPut_91_'+str(var)+'.csv ~/pub_sub_id/latencies/data/')
	run('sudo scp -i ~/.ssh/id_rsa siemens1:~/paho.mqtt.embedded-c/build/MQTTClient-C/samples/linux/perf_log_192.168.88.92_'+str(var)+'.csv ~/pub_sub_id/perf_log_192.168.88.92_87_'+str(var)+'.csv && sudo scp -i ~/.ssh/id_rsa siemens1:~/new_pub_sub_id/latencies/latency_87_'+str(var)+'.csv ~/pub_sub_id/latencies/ && sudo scp -i ~/.ssh/id_rsa siemens1:~/new_pub_sub_id/latencies/stddev_87_'+str(var)+'.csv ~/pub_sub_id/latencies/ && sudo scp -i ~/.ssh/id_rsa siemens1:~/new_pub_sub_id/latencies/pubJitter_87_'+str(var)+'.csv ~/pub_sub_id/latencies/data && sudo scp -i ~/.ssh/id_rsa siemens1:~/new_pub_sub_id/latencies/subJitter_87_'+str(var)+'.csv ~/pub_sub_id/latencies/data/ && sudo scp -i ~/.ssh/id_rsa siemens1:~/new_pub_sub_id/latencies/subPut_87_'+str(var)+'.csv ~/pub_sub_id/latencies/data/ && sudo scp -i ~/.ssh/id_rsa siemens1:~/new_pub_sub_id/latencies/pubPut_87_'+str(var)+'.csv ~/pub_sub_id/latencies/data/')
	run('sudo scp -i ~/.ssh/id_rsa siemens2:~/paho.mqtt.embedded-c/build/MQTTClient-C/samples/linux/perf_log_192.168.88.92_'+str(var)+'.csv ~/pub_sub_id/perf_log_192.168.88.92_88_'+str(var)+'.csv && sudo scp -i ~/.ssh/id_rsa siemens2:~/new_pub_sub_id/latencies/latency_88_'+str(var)+'.csv ~/pub_sub_id/latencies/ && sudo scp -i ~/.ssh/id_rsa siemens2:~/new_pub_sub_id/latencies/stddev_88_'+str(var)+'.csv ~/pub_sub_id/latencies/ && sudo scp -i ~/.ssh/id_rsa siemens2:~/new_pub_sub_id/latencies/pubJitter_88_'+str(var)+'.csv ~/pub_sub_id/latencies/data && sudo scp -i ~/.ssh/id_rsa siemens2:~/new_pub_sub_id/latencies/subJitter_88_'+str(var)+'.csv ~/pub_sub_id/latencies/data/ && sudo scp -i ~/.ssh/id_rsa siemens2:~/new_pub_sub_id/latencies/subPut_88_'+str(var)+'.csv ~/pub_sub_id/latencies/data/ && sudo scp -i ~/.ssh/id_rsa siemens2:~/new_pub_sub_id/latencies/pubPut_88_'+str(var)+'.csv ~/pub_sub_id/latencies/data/')
	run('sudo scp -i ~/.ssh/id_rsa siemens3:~/paho.mqtt.embedded-c/build/MQTTClient-C/samples/linux/perf_log_192.168.88.92_'+str(var)+'.csv ~/pub_sub_id/perf_log_192.168.88.92_89_'+str(var)+'.csv && sudo scp -i ~/.ssh/id_rsa siemens3:~/new_pub_sub_id/latencies/latency_89_'+str(var)+'.csv ~/pub_sub_id/latencies/ && sudo scp -i ~/.ssh/id_rsa siemens3:~/new_pub_sub_id/latencies/stddev_89_'+str(var)+'.csv ~/pub_sub_id/latencies/ && sudo scp -i ~/.ssh/id_rsa siemens3:~/new_pub_sub_id/latencies/pubJitter_89_'+str(var)+'.csv ~/pub_sub_id/latencies/data && sudo scp -i ~/.ssh/id_rsa siemens3:~/new_pub_sub_id/latencies/subJitter_89_'+str(var)+'.csv ~/pub_sub_id/latencies/data/ && sudo scp -i ~/.ssh/id_rsa siemens3:~/new_pub_sub_id/latencies/subPut_89_'+str(var)+'.csv ~/pub_sub_id/latencies/data/ && sudo scp -i ~/.ssh/id_rsa siemens3:~/new_pub_sub_id/latencies/pubPut_89_'+str(var)+'.csv ~/pub_sub_id/latencies/data/')'''


def get_ptp(var1,var2,var3):
	run("cd pub_sub_id && python3 ptp4.py "+str(var1)+" "+str(var2)+" "+str(var3))
