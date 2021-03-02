import math
from statistics import mean
import csv
import sys
import socket

csvfile = open('latencies/allLatencies.csv', newline='')
reader = csv.reader(csvfile)

sortedlist = sorted(reader, key=lambda row: row[1], reverse=False)
pubStore = []*88

#pubrate = [[10,1000],[10,500],[10,100],[10,50],[20,1000],[20,500],[20,100],[20,50],[50,1000],[50,500],[50,100],[50,50],[100,1000],[100,500],[100,100],[100,50],[500,1000],[500,500],[500,100],[500,50]]
#for x in pubrate:
	#pubStore.append([i,x[0],x[1]])
	#i = i+1


array = [32,64,128,256,512,1024,2048,4096,8192,16384,32768,655536]
pubrate = [1200, 1000, 900, 800, 700, 600, 500, 400, 300, 200, 100, 50]
#array = [10, 20, 50, 100, 200, 500, 700, 1000]
#pubrate = [1200, 1000, 900, 800, 700, 600, 500, 400, 300, 200, 100, 50]
i = 1
for x in array:
	for z in pubrate:
		pubStore.append([i,x,z])
		i = i+1

#final = []*int((len(sortedlist)/5))
#avg = 0
#sum = 0
#for row in range(0, 100, 5):
#	for x in range(row,row+5):
#		sum = sum + float(sortedlist[x][0])
#	avg = sum/5
#	final.append([sortedlist[row][1], avg])
#	avg = 0
#	sum = 0

with open("avg.csv", "a", newline='') as fd:
	writer = csv.writer(fd)
	for y in range(len(sortedlist)):
		for z in pubStore:
			if (str(z[0]) == str(sortedlist[y][1])):
				print("Average latency for pass "+str(sortedlist[y][1])+" = "+str(sortedlist[y][0]))
				writer.writerow([str(sortedlist[y][1]),str(z[1]),str(z[2]),str(sortedlist[y][0]), str(sortedlist[y][3])])
			else:
				continue

fd.close()
