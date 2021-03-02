import csv

latency_data1 = []
latency_data2 = []

num = [93]

title = ["Latency", "Array Size", "Publish Interval", "90th Percentile"]
def csvRead(filename):
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        count = 0
        #latency_data1.append(("Latency", "Array Size", "Publish Interval", "90th Percentile"))
        for row in csv_reader:
            average_latency = row[0]
            array, interval = row[1].split('_')
            ninetieth_percentile = row[3]
            latency_data1.append(((float(average_latency)*1000000), int(array), int(interval), (float(ninetieth_percentile)*1000000)))

def csvWrite(filename):
    with open(filename, "w+") as fd:
        writer = csv.writer(fd)
        for entries in latency_data1:
            writer.writerow([entries[1], entries[2], entries[0], entries[3]])


for z in num:
    csvRead('data/allLatencies.csv')
    latency_data1.sort(key = lambda x: (x[1], x[2]))
    latency_data1.insert(0,title)
    csvWrite('avg'+str(z)+'.csv')
    latency_data1.clear()
