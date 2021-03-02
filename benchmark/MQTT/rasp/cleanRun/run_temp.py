import sys
import os
from subprocess import Popen
from time import sleep
import datetime
import time


def run():
	array = [32, 64,128,256,512,1024,2048,4096,8192,16384,32768,63000]
	#array = [32]
#	array = [int(((num-41)/4)+1) for num in array if num>32]
	array = [int(((num-42)/4)+1) for num in array if num>32]
	pubrate = [1000, 900, 800, 700, 600, 500, 400, 300, 200, 100, 50, 30, 10, 7, 5, 3, 1]
#	pubrate = [600]
	i = 1
	final = []*250
	for x in array[::-1]:
		for z in pubrate[::-1]:
			final.append([x,z])
#	final = [[118, 100]]
	c = 0
#	print(final)
	for y in final:
		##p1 = Popen(["fab -H siemens1,siemens2,siemens3,siemens5,siemens6,siemens7,siemens8,siemens9,siemens10 -P run_subscribers:'"+str(i)+"'"], shell=True)
#		os.system("fab -H siemens7 run_tshark:'"+str(i)+"'")
#		os.system('nohup sudo tshark -f udp -Y "ip.src == 192.168.88.94 && ip.dst == 224.0.0.22" -Tfields -e ip.id -e frame.time > ~/pub_sub_id/tshark94_300_'+str(i)+'_2.txt 2>&1 &')
		os.system("fab -H siemens9 restart_broker")
		sleep(5)
		file_suffix_var = "{}_{}".format(y[0], y[1])
		p1 = Popen(["fab -H siemens7 run_subscribers:{}".format(file_suffix_var)], shell=True)

		'''p1 = Popen(["fab -H siemens7 run_subscribers:{}".format(file_suffix_var)+",1"], shell=True)
		p3 = Popen(["fab -H siemens8 run_subscribers:{}".format(file_suffix_var)+",2"], shell=True)
		p4 = Popen(["fab -H siemens10 run_subscribers:{}".format(file_suffix_var)+",3"], shell=True)
		p5 = Popen(["fab -H siemens5 run_subscribers:{}".format(file_suffix_var)+",4"], shell=True)
		p6 = Popen(["fab -H siemens1 run_subscribers:{}".format(file_suffix_var)+",5"], shell=True)
		p7 = Popen(["fab -H siemens2 run_subscribers:{}".format(file_suffix_var)+",6"], shell=True)
		p8 = Popen(["fab -H siemens3 run_subscribers:{}".format(file_suffix_var)+",7"], shell=True)'''

		sleep(5)
		#p2 = Popen(["cd ~/pub_sub_id && ./publish_mqtt --sample {} --interval {} --array_length {}".format(300, y[1], y[0])], shell=True)
		p2 = Popen(["./publish_mqtt --sample {} --interval {} --array_length {} --url opc.mqtt://192.168.88.95:1883".format(50, y[1], y[0])], shell=True)
		#p2 = Popen(["cd ~/paho.mqtt.embedded-c/build/MQTTClient-C/samples/linux && ./publisher --sample {} --interval {} --array_size {} --url 192.168.88.95 --qos 2".format(300, y[1], y[0])], shell=True)
		p1.wait()
		#p3.wait()
		#p4.wait()
		#p5.wait()
		
		#os.system("fab -H siemens7,siemens8,siemens10,siemens5,siemens1,siemens2,siemens3 calc_lat:'"+str(y[1])+","+str(file_suffix_var)+"' && fab -H pi@192.168.88.96 scp:'"+str(file_suffix_var)+"' && fab -H siemens7,siemens8,siemens10,siemens5,siemens1,siemens2,siemens3 install_collectd:'rm1'")
		#(this one)os.system("fab -H siemens7,siemens8 -P calc_lat:'"+str(y[1])+","+str(file_suffix_var)+"' && fab -H pi@192.168.88.96 scp:'"+str(file_suffix_var)+"' && fab -H siemens7,siemens8 -P install_collectd:'rm1'")
		os.system("fab -H siemens7 calc_lat:'{},{}' && fab -H pi@192.168.88.96 scp:'"+str(i)+"' && fab -H siemens7 -P install_collectd:'rm1'".format(y[1], file_suffix_var))
		#os.system("fab -H pi@192.168.88.96 scp:'"+str(i)+"' && fab -H siemens9 install_collectd:'rm'")
		##os.system("fab -H siemens1,siemens2,siemens3,siemens5,siemens6,siemens7,siemens8,siemens9,siemens10 -P calc_lat:'"+str(y[1])+","+str(i)+"'")
		i = i+1
#		c = c + 1
		p2.wait()
#		os.system("ps -A | grep tshark | awk \'{print $1}\' | sudo xargs kill")
#		os.system('ssh siemens7 "ps -A | grep tshark | awk \'{print $1}\' | sudo xargs kill"')
		sleep(5)
#    print (final)
        #for x in array:
		#for y in pubrate:
			#p1 = Popen(["fab -H siemens1,siemens2,siemens3,siemens5,siemens6,siemens7,siemens8,siemens9,siemens10 -P run_subscribers:'"+str(i)+"'"], shell=True)
			#sleep(15)
			#p2 = Popen(["cd pub_sub_id && ./publish_time -sample 50 -interval "+str(y)+" -write_rate "+str(y)+" -array_size "+str(x)], shell=True)
			#p1.wait()
			#os.system("fab -H siemens1,siemens2,siemens3,siemens5,siemens6,siemens7,siemens8,siemens9,siemens10 -P calc_lat:'"+str(y)+","+str(i)+"'")
			#i = i+1
			#p2.wait()

run()
