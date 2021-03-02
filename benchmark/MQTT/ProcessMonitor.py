#!/usr/bin/python3
# 
# Author: Zhuangwei Kang
# 

import os, sys
import psutil
import argparse
import pandas as pd
import subprocess
from decimal import Decimal
import json
import time

WORK_PATH = '/home/pi/DDSExp/rtiperftest'

class ProcessMonitor(object):
    def __init__(self, pname=None, pid=None, session=None):
        self.__pid = pid
        self.__pname = pname.lower()
        self.__session = session

        self.__last_read = None
        self.__last_sys_cpu_read = None
        self.__last_process_cpu_read = None
        self.__last_netstat_read = None

    def init_process(self):
        try:
            if self.__pid:
                self.__process = psutil.Process(pid=self.__pid)
                return True
            else:
                self.__pid = self.getPid()
                if self.__pid:
                    self.__process = psutil.Process(pid=self.__pid)
                    return True
                else:
                    return False
        except Exception:
            return False

    def getPid(self):
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
                if self.__pname in pinfo['name'].lower():
                    return pinfo['pid']
            except Exception:
                # TODO: handle exception
                return None
        return None
        
    
    def __getAllowedCPUs(self):
        """
        :return (list) return a list of cpu id that were assigned to process
        """
        allowed_cpu = subprocess.check_output('cat /proc/%d/status | grep Cpus_allowed_list | cut -f 2 -d ":"' % self.__pid, shell=True).decode().strip()
       
        cpus = []
        allowed_cpu = allowed_cpu.split(',')
        for item in allowed_cpu:
            if '-' in item:
                start = int(item.split('-')[0])
                end = int(item.split('-')[1])
                cpus.extend(range(start, end+1))
            else:
                cpus.append(item)

        return cpus

    def __get_total_cpu_jiffies(self):
        """
        :return (int) total jiffies of allowed CPUs
        """
        cpus = self.__getAllowedCPUs()
        total_cpu = 0
        for i in cpus:
            cmd = 'cat /proc/stat | grep cpu%s' % str(i)
            result = subprocess.check_output(cmd, shell=True).decode().split(' ')
            total_cpu += sum(list(map(lambda x: int(x), list(filter(lambda x: x != ' ', result))[1:])))
        return total_cpu

    def __get_process_jiffies(self):
        """
        :return (int) utime+stime+cutime+cstime of the process in jiffies
        """
        
        # this gives you cpu times in seconds
        # return sum(self.__process.cpu_times())

        cmd = 'cut -f 14,15,16,17 -d " " /proc/%d/stat' % self.__pid
        result = subprocess.check_output(cmd, shell=True).decode().split(' ')
        result = [int(x) for x in result]
        return sum(result)
      
    def getCpuPercent(self):
        """
        :return (float) CPU usage rate since last call
        """

        # this gives you instant cpu percent
        # return self.__process.cpu_percent(0.1)
         
        cpu_jiffies = self.__get_total_cpu_jiffies() # current cpu time
        process_jiffies = self.__get_process_jiffies() # current process specific time

        percent = 0.0
        if self.__last_read:
            elapsed_cpu_jiffies = cpu_jiffies - self.__last_sys_cpu_read
            elasped_process_jiffies = process_jiffies - self.__last_process_cpu_read
            percent = 100*elasped_process_jiffies/elapsed_cpu_jiffies

        self.__last_sys_cpu_read = cpu_jiffies
        self.__last_process_cpu_read = process_jiffies

        return round(percent, 2)

    def getMemory(self, field='rss'):
        return round(self.__process.memory_percent(field), 4)

    def __getNetStats(self):
        """
        :return: (dict) cumulative network statistics of each interface
        """
        cmd = "cat /proc/%d/net/dev" % self.__pid
        net_metrics = subprocess.check_output(cmd, shell=True).decode()
        net_metrics = net_metrics.split('\n')

        fields = list(set(net_metrics[1].split('|')[1].split(' ')))
        fields.remove('')

        netstate = {}
        
        # Receive: bytes, packets, errs, drop, fifo, frame, compressed, multicast
        # Transmit: bytes,  packets, errs, drop, fifo, colls, carrier, compressed

        for i in range(2, len(net_metrics)):
            if ':' not in net_metrics[i]:
                continue
            line = net_metrics[i].split(':')
            data = line[1].split(' ')
            data = list(filter(lambda x: x != '', data))
            data = [int(x) for x in data]
            netstate.update({
                line[0].strip(): {
                    'rx': data[:8],
                    'tx': data[8:]
                }
            })
        return netstate
    
    def getTxRxRate(self):
        """
        :return (dict) TX, RX rate since last call
        """
        current_stat = self.__getNetStats()
        now = time.time()
        result = {}
        for interface in current_stat:
            result.update({
                interface: {
                    'rx': [0]*len(current_stat[interface]['rx']),
                    'tx': [0]*len(current_stat[interface]['tx'])
                }
            })

        if self.__last_read:
            for interface in current_stat:
                for x in current_stat[interface]:
                    result[interface][x] = [round((x1-x2)/(now-self.__last_read), 2) for (x1, x2) in zip(current_stat[interface][x], self.__last_netstat_read[interface][x])]

        self.__last_read = now
        self.__last_netstat_read = current_stat
       
        return result
    
    def processMonitor(self):
        filePath = '%s/%s.csv' % (WORK_PATH, self.__session)
        with open(filePath, 'w') as f:
            f.write('cpu,memory,rx_bytes,rx_packets,rx_errs,rx_drop,tx_bytes,tx_packets,tx_errs,tx_drop\n')
        
        while self.getPid():
            try:
                cpu = self.getCpuPercent()
                memory = self.getMemory()
                netstat_rate =  self.getTxRxRate()
            except Exception: # in case perftest_cpp finished
                break
    
            tx_sum = [0] * 4
            rx_sum = [0] * 4

            # add up tx rx rate of each interface
            for interface in netstat_rate:
                if interface != 'eth0': # only need 'eth0' in this experiment
                    continue
                rx = netstat_rate[interface]['rx'][:5]
                rx_sum = [rx_sum[i]+rx[i] for i in range(4)]

                tx = netstat_rate[interface]['tx'][:5]
                tx_sum = [tx_sum[i]+tx[i] for i in range(4)]
            
            rx_sum.extend(tx_sum)
            netstat_rate = ','.join([str(x) for x in rx_sum])
            
            with open(filePath, 'a') as f:
                f.write('%f,%f,%s\n' % (cpu, memory, netstat_rate))
            
            time.sleep(5)
    
    def processTestData(self):
        file_path = '%s/%s.csv' % (WORK_PATH, self.__session)
        df = pd.DataFrame.from_csv(file_path, index_col=None)

        avg = df.mean(axis=0).to_frame().T
        ninty_per = df.quantile(q=0.9, axis=0).to_frame().T
        fifty_per = df.quantile(q=0.5, axis=0).to_frame().T
        
        pub_rate = float(self.__session.split('-')[0])
        data_len = int(self.__session.split('-')[1])

        def add_col(dframe):
            dframe['dataLen'] = data_len
            dframe['pubRate'] = pub_rate
            return dframe
        
        avg = add_col(avg)
        ninty_per = add_col(ninty_per)
        fifty_per = add_col(fifty_per)

        def to_csv(dframe, dfile):
            if not os.path.exists(dfile):
                dframe.to_csv(dfile, index=False)
            else:
                dframe.to_csv(dfile, index=False, mode='a', header=False)

        avg_file = '%s/avg.csv' % WORK_PATH
        to_csv(avg, avg_file)

        fifty_file = '%s/50th.csv' % WORK_PATH
        to_csv(fifty_per, fifty_file)

        ninty_file = '%s/90th.csv' % WORK_PATH
        to_csv(ninty_per, ninty_file)

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--session', type=str, required=True, help='The session ID of the process monitor.')
    parser.add_argument('--pname', type=str, required=False, help='The process name.')
    parser.add_argument('--pid', type=int, required=False, help='Process ID')
    args = parser.parse_args()

    if args.pname:
        client = ProcessMonitor(pname=args.pname, session=args.session)
    elif args.pid:
        client = ProcessMonitor(pid=args.pid, session=args.session)
    else:
        assert False, "Please provide either process name or process ID"

    if client.init_process():
        client.processMonitor()
        client.processTestData()
