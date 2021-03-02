from statistics import mean
from statistics import stdev
import csv
import sys
import socket
import numpy as np
import sys
import datetime
import json
import time
import subprocess
import threading


subValue = [[],[],[],[],[],[],[],[],[],[]]

pub_int = float(sys.argv[1])

pubJit = []*300
subJit = []*300
#def parse_ptp_offset(fname):
#    with open(fname) as f:
#        data = f.readlines()
#    data = [line.split(' ') for line in data]
#
#    rm_flg = 0
#    for i, item in enumerate(data[:]):
#        try:
#            data[i] = int([x for x in item if x != ''][8])
#        except:
#            data[i] = 0
#            rm_flg += 1
#    return sum(data)/(len(data)-rm_flg)/1000

if __name__ == "__main__":

	csvfile = open('/home/pi/cleanRun/pubsub/perf_log_192.168.88.92_'+str(sys.argv[2])+'.csv', newline='')
	reader = csv.reader(csvfile)
	i = 0
	change_ip = 0
	#sortedlist = sorted(reader, key=lambda row: row[1], reverse=True)


#	pub_parse = parse_ptp_offset("ptp4l_pub_"+str(sys.argv[2])+".log")
#	sub_parse = parse_ptp_offset("ptp4l_sub_"+str(sys.argv[2])+".log")
#	ptp = sub_parse - pub_parse

	first = 0
	for row in reader:
		if(first == 0):
			val = (float(row[3]) - float(row[2]))/(1000000000) #+ ptp/1000000000
			#val = ((float(row[3])-float(row[2]))-10000000)/10000000 - 1/pub_int
			subValue[change_ip+1].append(val)
			subValue[change_ip].append(row[1])
			i = i + 1
			first = first + 1
		elif(first != 0):
			if(row[1] == subValue[change_ip][i-1]):
				val = (float(row[3]) - float(row[2]))/(1000000000) #+ ptp/1000000000
				#val = ((float(row[3])-float(row[2]))-10000000)/10000000 - 1/pub_int
				subValue[change_ip+1].append(val)
				subValue[change_ip].append(row[1])
				i = i + 1
			else:
				change_ip = change_ip + 2
				i = 0
				val = (float(row[3]) - float(row[2]))/(1000000000) #+ ptp/1000000000
				#val = ((float(row[3])-float(row[2]))-10000000)/10000000 - 1/pub_int
				subValue[change_ip+1].append(val)
				subValue[change_ip].append(row[1])
				i = i + 1
	num_ip = change_ip/2

	csvfile = open('/home/pi/cleanRun/pubsub/perf_log_192.168.88.92_'+str(sys.argv[2])+'.csv', newline='')
	read = csv.reader(csvfile)
	data = list(read)
	row_count = len(data)
	print(row_count)
	for x in range(row_count - 1):
		pubJitter = (float(data[x+1][2]) -float(data[x][2]))/1000000
		subJitter = (float(data[x+1][3]) - float(data[x][3]))/1000000
		pubJit.append(pubJitter)
		subJit.append(subJitter) 

	subPut = row_count/((float(data[row_count - 1][3]) - float(data[0][3]))/1000000000)
	print("Sub: "+str(subPut))
	pubPut = row_count/((float(data[row_count - 1][2]) - float(data[0][2]))/1000000000)
	print("Pub: "+str(pubPut))

	if(change_ip > 0):
		counter = 0
		for count in range(0,int(num_ip)+1):
			avg = mean(subValue[counter+1])
			print("Average latency ("+subValue[counter][0]+") = "+str(avg))
			file1 = open("latencies/latency_93_"+str(sys.argv[2])+".csv","w")
			file1.write(str(avg)+','+str(sys.argv[2])+','+str(socket.getfqdn())+'\n')
			file1.close()
			counter = counter + 2
	else:
		avg = mean(subValue[1])
		std = stdev(subValue[1])
		perc = np.percentile(subValue[1], 90)
		print("Average latency, stddev, 90th percentile ("+subValue[0][0]+") = "+str(avg)+", "+str(std)+", "+str(perc))
		file1 = open("latencies/latency_93_"+str(sys.argv[2])+".csv","w")
		file1.write(str(avg)+','+str(sys.argv[2])+','+str(socket.getfqdn())+','+str(perc)+'\n')
		file1.close()

		file2 = open("latencies/stddev_93_"+str(sys.argv[2])+".csv","w")
		file2.write(str(std)+','+str(sys.argv[2])+','+str(socket.getfqdn())+'\n')
		file2.close()

		file3 = open("latencies/pubJitter_93_"+str(sys.argv[2])+".csv","w")
		for y in pubJit:
			file3.write(str(y)+','+str(sys.argv[2])+','+str(socket.getfqdn())+'\n')
		file3.close()

		file4 = open("latencies/subJitter_93_"+str(sys.argv[2])+".csv","w")
		for z in subJit:
			file4.write(str(z)+','+str(sys.argv[2])+','+str(socket.getfqdn())+'\n')
		file4.close()

		file5 = open("latencies/subPut_93_"+str(sys.argv[2])+".csv","w")
		file5.write(str(subPut)+','+str(sys.argv[2])+','+str(socket.getfqdn())+'\n')
		file5.close()

		file6 = open("latencies/pubPut_93_"+str(sys.argv[2])+".csv","w")
		file6.write(str(pubPut)+','+str(sys.argv[2])+','+str(socket.getfqdn())+'\n')
		file6.close()
