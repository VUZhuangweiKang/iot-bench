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

#pub_int = float(sys.argv[1])

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

	csvfile = open('./serialize_'+str(sys.argv[1])+'.csv', newline='')
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
	
	avg = mean(subValue[1])
	std = stdev(subValue[1])
	perc = np.percentile(subValue[1], 90)
	print("Average latency, stddev, 90th percentile ("+subValue[0][0]+") = "+str(avg)+", "+str(std)+", "+str(perc))
	file1 = open("./serial_"+str(sys.argv[1])+".csv","w")
	file1.write("Serialization time,data type,standard deviation,90th percentile time\n")
	file1.write(str(avg)+','+str(sys.argv[1])+','+str(std)+','+str(perc)+'\n')
	file1.close()

