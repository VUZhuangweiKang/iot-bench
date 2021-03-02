#!/usr/bin/python3
import os, sys
from multiprocessing.dummy import Pool
import argparse
import subprocess
from threading import Thread
import time
import traceback
import random
import json
from decimal import Decimal
import numpy as np
import pandas as pd

PLATFORM = ''

class RTIPerfTest(object):
    def __init__(self, workPath, profile):
        self.workPath = workPath
        self.expID = profile['id']
        self.pubs = profile['pubs']
        self.subs = profile['subs']
        self.pubRate = profile['pubRate']
        self.dataLen = profile['dataLen']
        self.parameters = profile['parameters']

    @staticmethod
    def getHostAddress(svr_str):
        # parse entered server string
        svrs = svr_str.split(',')
        with open('server_list.json') as f:
            servers = json.load(f)[PLATFORM]
        if len(svrs) == 1: # input server string is a single server
            return servers[svrs[0]]
        else:
            return [servers[svr] for svr in svrs]

    def __getHosts(self):
        hosts = self.pubs[:]
        hosts.extend(self.subs)
        return hosts

    def limitCPU(self, host, cores):
        """
        :cores (list) limit the perftest_cpp to use specified cores
        """
        cores = [str(x) for x in cores]
        cores = ','.join(cores)
        os.system('ssh %s "pgrep perftest_cpp | xargs taskset -cp %s"' % (self.getHostAddress(host), cores))

    def startMonitor(self, host, pubRate=None, dataLen=None):
        cmd = 'ssh %s "cd %s/rtiperftest && ./ProcessMonitor.py -s %s-%s --pname perftest_cpp"' % (self.getHostAddress(host), self.workPath, pubRate, dataLen)
        temp = lambda: os.system(cmd)
        thr = Thread(target=temp, daemon=False)
        thr.start()

    def cmdFactory(self, svr, isPub, id, logfile, dataLen, pub_rate=None):
        build_cmd = lambda details: 'nohup ssh %s "cd %s/rtiperftest && ./perftest_cpp %s" | grep Length >> %s 2>&1 &' % (self.getHostAddress(svr), self.workPath, details, logfile)

        def integrateParms(input):
            details = []

            for key in input:
                if type(input[key]) is bool:
                    if input[key] is True:
                        details.append("%s" % key)
                    else:
                        continue
                else:
                    # batchSize is only enabled in throughputTest and must be as least two times of dataLen
                    if key == '-batchSize' and input[key] != 0:
                        details.append('%s %s' % (key, str(2*dataLen)))
                    else:
                        details.append('%s %s' % (key, str(input[key])))
            return details

        common_base = ' '.join(integrateParms(self.parameters['common']))
        if isPub:
            details = integrateParms(self.parameters['pub'])

            num_iter = int(90 * ((1e6*950/8)/dataLen))
            latency_count = int(num_iter/200)

            if pub_rate and pub_rate != 0:
                details.insert(0, '-pub -pubRate %s:spin -dataLen %d -pidMultiPubTest %d -numIter %d -latencyCount %d' % (pub_rate, dataLen, id, num_iter, latency_count))
            else:
                details.insert(0, '-pub -dataLen %d -pidMultiPubTest %d -numIter %d -latencyCount %d' % (dataLen, id, num_iter, latency_count))
            details = '%s %s' % (' '.join(details), common_base)
        else:
            details = integrateParms(self.parameters['sub'])
            details.insert(0, '-sub -dataLen %d -sidMultiSubTest %d' % (dataLen, id))
            details = '%s %s' % (' '.join(details), common_base)
        return build_cmd(details)

    def runSubscribers(self, dataLen, pubRate):
        # run subscribers
        for i, sub in enumerate(self.subs):
            cmd = self.cmdFactory(sub, False, i, 'sub_%s.log' % sub, dataLen)
            os.system(cmd)
            time.sleep(0.3)
            self.limitCPU(sub, [1])
            self.startMonitor(sub, pubRate=pubRate, dataLen=dataLen)

    def runPublishers(self, pub_rate, dataLen):
        for i, pub in enumerate(self.pubs):
            # if pubs>1, limit pubRate
            if len(self.pubs) > 1:
                bw = 950
                pub_rate = int((bw/(8*len(self.pubs)))*1024*1024/dataLen)

            # run publisher
            cmd = self.cmdFactory(pub, True, i, 'pub_%s.log' % pub, dataLen, pub_rate)

            # only publisher with pid=0 can run latencyTest
            if i != 0 and '-latencyTest' in cmd:
                cmd = cmd.replace('-latencyTest', '')
            print(cmd)
            os.system(cmd)
            time.sleep(0.3)
            self.limitCPU(pub, [1])
            self.startMonitor(pub, pubRate=pub_rate, dataLen=dataLen)

    def log2csv(self, log, fields, csvPath):
        with open(csvPath, 'a') as f:
            for i, line in enumerate(log):
                data = []
                for fld in fields:
                    val = line.split(fld)[1].strip('\n').strip()
                    avoid = [' ', '', '\n', 'us', '%']
                    for x in avoid:
                        val = val.replace(x, '')
                    data.insert(0, val)
                    line = line.split(fld)[0]
                data = '%d,%s\n' % (self.pubRate[int(i/len(self.dataLen))], ','.join(data))
                f.write(data)

    def parseSubLog(self, subLog):
        with open(subLog) as f:
            sub_data = f.readlines()

        subCSV = '%s.csv' % subLog.split('.')[0]
        with open(subCSV, 'w') as f:
            f.write('pub_rate(samples/s),data_length,packets,packets/s(ave),Mbps(ave),lost,CPU(%)\n')
        fields = ['CPU:', 'Lost:', 'Mbps(ave):', 'Packets/s(ave):', 'Packets:', 'Length:']
        self.log2csv(sub_data, fields, subCSV)

    def parsePubLog(self, pubLog):
        with open(pubLog) as f:
            pub_data = f.readlines()

        pubCSV = '%s.csv' % pubLog.split('.')[0]
        with open(pubCSV, 'w') as f:
            f.write('pub_rate(ms),data_length,latency(ave),latency(std),latency(min),latency(max),latency(50%),latency(90%),latency(99%),latency(99.99%),latency(99.9999%),CPU(%)\n')
        fields = ['CPU:', '99.9999%', '99.99%', '99%', '90%', '50%', 'Max', 'Min', 'Std', 'Latency: Ave', 'Length:']
        self.log2csv(pub_data, fields, pubCSV)

    def orgDir(self):
        # copy experiment monitor file to manager
        for host in self.__getHosts():
            os.mkdir('./monitor/%s' % host)
            cmd = 'scp %s:~/DDSExp/rtiperftest/*.csv ./monitor/%s/' % (self.getHostAddress(host), host)
            os.system(cmd)
            # remove old files
            cmd = 'ssh %s "rm %s/rtiperftest/*.csv"' % (self.getHostAddress(host), self.workPath)
            os.system(cmd)

        # create a directory for the past experiment
        pastExp = './%s' % self.expID
        os.mkdir(pastExp)
        # mv experiment results to the directory
        os.system('cp ./profile.json %s' % pastExp)
        os.system('mv pub*.csv %s' % pastExp)
        os.system('mv sub*.csv %s' % pastExp)
        os.system('mv *.log %s' % pastExp)
        os.system('mv monitor %s' % pastExp)

    def blockMain(self):
        for host in self.__getHosts():
            cmd = 'ssh %s "pgrep perftest_cpp"' % self.getHostAddress(host)
            try:
                while len(subprocess.check_output(cmd, shell=True).decode()) > 0:
                    time.sleep(3)
            except Exception:
                pass

def startExp(tid, profile):
    if PLATFORM == 'Armv7l':
        WORK_PATH = '/home/pi/DDSExp'
    else:
        WORK_PATH = '/home/ubuntu/DDSExp'

    client = RTIPerfTest(WORK_PATH, profile)
    os.mkdir('./monitor')

    for pub_rate in client.pubRate:
        for dataLength in client.dataLen:
            client.runSubscribers(dataLength, pub_rate)
            client.runPublishers(pub_rate, dataLength)
            client.blockMain()

    for pub in client.pubs:
        client.parsePubLog('pub_%s.log' % pub)

    for sub in client.subs:
        client.parseSubLog('sub_%s.log' % sub)

    time.sleep(1)
    client.orgDir()

def main(servers, platform):
    global PLATFORM

    if platform == 'AMD64':
        interface = 'em1'
        PLATFORM = 'AMD64'
    else:
        interface = 'eth0'
        PLATFORM = 'Armv7l'

    df = pd.read_csv('%sExpSchedule.csv' % PLATFORM)
    servers_bk = servers[:]

    for index, row in df.iterrows():
        if index not in [3]:
            continue
        servers = servers_bk[:]
        # load profile template
        with open('ProfileTemplate.json') as f:
            profile = json.load(f)

        profile['id'] = int(index)

        # randomly select publishers and subscribers
        for _ in range(row['Publisher']):
            random_index = random.randint(0, len(servers)-1)
            profile['pubs'].append(servers[random_index])
            del servers[random_index]
        
        for _ in range(row['Subscriber']):
            random_index = random.randint(0, len(servers)-1)
            profile['subs'].append(servers[random_index])
            del servers[random_index]     
        
        # profile['pubs'] = ['u_isis2']
        # profile['subs'] = ['u_isis5']

        profile['parameters']['common'].update({
            '-nic': interface,
            '-multicast': row['Multicast'],
            '-durability': row['Durability'],
            '-useReadThread': row['UseReadThread']
        })

        # swicth to qos file which history == 50
        if row['Durability'] == 2 and row['History'] == '50':
            profile['parameters']['common']['-qosFile'] = 'perftest_qos_profiles_history.xml'

        # choose heartbeat
        if row['Heartbeat'] == 'slow':
            profile['parameters']['common']['-qosFile'] = 'perftest_qos_profiles_heartbeat_slow.xml'
        if row['Heartbeat'] == 'fast':
            profile['parameters']['common']['-qosFile'] = 'perftest_qos_profiles_heartbeat_fast.xml'
        
        if int(row['LatencyBudget']) != 0:
            profile['parameters']['common']['-qosFile'] = 'perftest_qos_profiles_latency_budget.xml'
        
        profile['parameters']['pub'].update({
            '-numSubscribers': row['Subscriber'],
            '-latencyTest': row['LatencyTest'],
            '-sendQueueSize': int(row['SendQueueSize']),
            '-enableTurboMode': row['EnableTurboMode'],
            '-enableAutoThrottle': row['EnableAutoThrottle']
        })

        # spin is ignored when AutoThrottle is enabled
        if (not row['EnableAutoThrottle']) and int(row['Spin']) != 0:
            profile['parameters']['pub'].update({
                '-spin': int(row['Spin'])
            })

        profile['parameters']['sub'].update({
            '-numPublishers': row['Publisher']
        })
        
        # only publisher with pid=0 can run latency Test
        if row['Publisher']  > 1 and row['LatencyTest']:
            del profile['parameters']['sub']['-numPublishers']

        with open('profile.json', 'w') as f:
            json.dump(profile, f)
        
        startExp(index, profile)


if __name__ == "__main__":
    amd64 = ['u_isis2', 'u_isis5', 'u_isis6', 'u_isis7', 'u_isis11', 'u_isis12', 'u_isis13', 'u_isis15']
    armv7l = ['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8']
    if sys.argv[1] == "AMD":
        main(amd64, 'AMD64')
    else:
        main(armv7l, 'Armv7l')
