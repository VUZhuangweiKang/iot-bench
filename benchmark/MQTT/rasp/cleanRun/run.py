import os


#os.system('cp ~/pub_sub_id/latencies/allLatencies.csv ./ && cp ~/pub_sub_id/latencies/data/all* ./latencies/')
#os.system('sudo cp ~/pub_sub_id/latencies/data/all* ./latencies/')
os.system('python3 avgLatency.py')
os.system('python3 pubPut.py')
os.system('python3 subPut.py')
os.system('python3 pubJit.py')
os.system('python3 subJit.py')
os.system('python3 stddev.py')
