#!/usr/bin/python3
import os
from multiprocessing.dummy import Pool
import argparse
import subprocess
from threading import Thread
import time
import traceback
import json
from decimal import Decimal
import pandas as pd


class RTIPerfTest(object):
    def __init__(self, workPath, expProfile):
        self.workPath = workPath
        with open(expProfile) as f:
            profile = json.load(f)
            self.expID = profile['id']
            self.pubs = profile['pubs']
            self.subs = profile['subs']
            self.pubRate = profile['pubRate']
            self.dataLen = profile['dataLen']

    @staticmethod
    def get_svr_address(svr_str):
        # parse entered server string
        svrs = svr_str.split(',')
        with open('server_list.json') as f:
            servers = json.load(f)
        servers = servers['raspberry']
        if len(svrs) == 1: # input server string is a single server
            return servers[svrs[0]]
        else:
            return [servers[svr] for svr in svrs]

    def __getHosts(self):
        hosts = self.pubs[:]
        hosts.extend(self.subs)
        return hosts

    def limitCPU(self, host, cores, exec_name):
        """
        :cores (list) limit the perftest_cpp to use specified cores
        """
        cores = [str(x) for x in cores]
        cores = ','.join(cores)
        cmd = 'ssh -i /home/pi/.ssh/id_rsa pi@%s "pgrep %s | xargs taskset -cp %s"' % (self.get_svr_address(host), exec_name, cores)
        #print(cmd)
        os.system(cmd)

    def start_monitor_sub(self, host, real_pub, real_data):
        cmd = 'sudo ssh -i /home/pi/.ssh/id_rsa siemens7 "cd /home/pi/cleanRun/ && ./ProcessMonitor.py -s %s-%s --pname subscriber"' % (real_pub, real_data)
        temp = lambda: os.system(cmd)
        thr = Thread(target=temp, daemon=False)
        thr.start()

    def start_monitor_pub(self, host, real_pub, real_data):
        cmd = 'sudo ssh -i /home/pi/.ssh/id_rsa siemens6 "cd /home/pi/cleanRun/ && ./ProcessMonitor.py -s %s-%s --pname publisher"' % (real_pub, real_data)
        temp = lambda: os.system(cmd)
        thr = Thread(target=temp, daemon=False)
        thr.start()

    def runSubscribers(self, dataLen, pubRate, realData, realPub):
        # run subscribers
        for i, sub in enumerate(self.subs):
            #cmd = self.cmdFactory(sub, False, i, 'sub_%s.log' % sub, dataLen)
            cmd = 'sudo nohup ssh -i /home/pi/.ssh/id_rsa pi@%s "cd /home/pi/cleanRun/pubsub && ./subscriber --sample 300 --url 192.168.88.95 --qos 2 && cat perf_log_mqtt_192.168.88.92.csv > perf_log_192.168.88.92_%s_%s.csv && python3 calcLatency_MQTT.py %s_%s" >> data.log 2>&1 &' % (self.get_svr_address(sub),realPub,realData,realPub,realData)
            #print(cmd)
            os.system(cmd)
            time.sleep(2)
            self.limitCPU(sub, [1], 'subscriber')
            self.start_monitor_sub(sub, realPub, realData)
        #self.scp_cat()

    def runPublishers(self, pub_rate, dataLen, realData, realPub):
        for i, pub in enumerate(self.pubs):
            # run publisher
            #cmd = self.cmdFactory(pub, True, i, 'pub_%s.log' % pub, dataLen, pub_rate)
            cmd = 'sudo nohup ssh -i /home/pi/.ssh/id_rsa siemens6 "cd /home/pi/cleanRun/pubsub && ./publisher --sample 10000 --interval %s --array_size %s --url 192.168.88.95 --qos 2" >> data.log 2>&1 &' % (pub_rate, dataLen)
            #print(cmd)
            os.system(cmd)
            time.sleep(2)
            self.limitCPU(pub, [1], 'publisher')
            self.start_monitor_pub(pub, realPub, realData)

    def scp_cat(self):
        for i, sub in enumerate(self.subs):
            os.system('sudo scp -i /home/pi/.ssh/id_rsa pi@%s:/home/pi/cleanRun/pubsub/perf_log* ./pubsub/ && sudo scp -i /home/pi/.ssh/id_rsa pi@%s:/home/pi/cleanRun/pubsub/latencies/* ./pubsub/latencies/ && mkdir data/process/%s && sudo scp -i /home/pi/.ssh/id_rsa pi@%s:~/cleanRun/data/process/* ./data/process/%s/ && sudo scp -i /home/pi/.ssh/id_rsa pi@192.168.88.92:~/cleanRun/data/process/* ./data/process/92/ && sudo ssh -i /home/pi/.ssh/id_rsa pi@%s "rm /home/pi/cleanRun/pubsub/perf_log* && rm /home/ubuntu/cleanRun/pubsub/latencies/*"' % (self.get_svr_address(sub), self.get_svr_address(sub), self.get_svr_address(sub), self.get_svr_address(sub), self.get_svr_address(sub), self.get_svr_address(sub)))
            os.system('sudo cat pubsub/latencies/latency* > data/allLatencies.csv && sudo cat pubsub/latencies/std* > allStdDev.csv && sudo cat pubsub/latencies/subJit* > data/allSubJits.csv && sudo cat pubsub/latencies/pubJit* > data/allPubJits.csv && sudo cat pubsub/latencies/subPut* > data/allSubPuts.csv && sudo cat pubsub/latencies/pubPut* > data/allPubPuts.csv')
        #os.system('python3 run.py')


    def block_main_pub(self):
        for host in self.__getHosts():
            cmd = 'sudo ssh -i /home/pi/.ssh/id_rsa siemens6 "pgrep publisher"'
            try:
                while len(subprocess.check_output(cmd, shell=True).decode()) > 0:
                    time.sleep(3)
            except Exception:
                pass


    def block_main_sub(self):
        for i, sub in enumerate(self.subs):
            cmd = ('sudo ssh -i /home/pi/.ssh/id_rsa pi@%s "pgrep subscriber"' % (self.get_svr_address(sub)))
            try:
                while len(subprocess.check_output(cmd, shell=True).decode()) > 0:
                    time.sleep(3)
            except Exception:
                pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--profile', help='experiment profile path', type=str, default='profile.json')
    args = parser.parse_args()
    profile = args.profile

    pub_rate = [0.0, 1.0, 1.1111, 1.25, 1.43, 1.67, 2, 2.5, 3.3333, 5.0, 10.0]
    real_pub = [0,1000,900,800,700,600,500,400,300,200,100]
    real = [64,128,256,512,1024,2048,4096,8192,16384,32768]
    #real = [512,16384]
    #pub_rate = [2]
    #real_pub = [500]
    array = [int(((num-40)/4)+1) for num in real]
    WORK_PATH = '/home/pi/cleanRun'
    client = RTIPerfTest(WORK_PATH, profile)
    
    monitor_dir = '%s/mqtt/monitor' % WORK_PATH
    os.mkdir(monitor_dir)
    tally = 0
    start = 0
    for i in pub_rate:
        for j in array:
            client.runSubscribers(j, i, real[start], real_pub[tally])
            client.runPublishers(i, j, real[start], real_pub[tally])
            client.block_main_pub()
            client.block_main_sub()
            os.system('sudo ssh -i /home/pi/.ssh/id_rsa siemens9 "sudo systemctl restart mosquitto.service"')
            print('Done with round '+str(tally)+'-'+str(start))
            if (start < 9):
                start = start + 1
            else:
                start = 0
                tally = tally + 1

    '''for pub in client.pubs:
        client.parsePubLog('pub_%s.log' % pub)
    
    for sub in client.subs:
        client.parseSubLog('sub_%s.log' % sub)'''


    time.sleep(5)
    client.scp_cat()
    os.system('sudo python3 run.py')
