import csv

latency_data1 = []
latency_data2 = []

title = ["Throughput", "Array Size", "Publish Interval"]

num = [93]

def csvRead(filename):
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        count = 0
        #latency_data1.append(("Throughput", "Array Size", "Publish Interval"))
        for row in csv_reader:
            average_latency = row[0]
            array, interval = row[1].split('_')
            #array = ((int(array)-1)*4)+40
            latency_data1.append((float(average_latency)*int(interval)*8, int(array), int(interval)))

def csvWrite(filename):
    with open(filename, "w+") as fd:
        writer = csv.writer(fd)
        for entries in latency_data1:
            writer.writerow([entries[1], entries[2], entries[0]])

for z in num:
    csvRead('data/allPubPuts.csv')
    latency_data1.sort(key = lambda x: (x[1], x[2]))
    latency_data1.insert(0,title)
    csvWrite('data/pubPuts.csv')
    latency_data1.clear()
