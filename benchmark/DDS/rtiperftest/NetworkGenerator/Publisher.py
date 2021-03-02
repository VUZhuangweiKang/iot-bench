#!/usr/bin/python3
import os
import argparse

ARM_BW=95
AMD_BW=950
DATA_LEN=4096

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--platform', help='Platform', choices=['Arm', 'AMD'])
    parser.add_argument('-b', '--bandwidth', help='Percent of maximum bandwidth will be used.', type=int)
    parser.add_argument('-t', '--exe_time', help='Executiom Time(s)', default=36000, type=int)
    parser.add_argument('-d', '--dataLen', help='Data Length(bytes)', default=16384, type=int)

    args = parser.parse_args()
    dataLen = args.dataLen

    if args.platform == 'Arm':
        pubRate = int((args.bandwidth/100)*(ARM_BW*1024*1024/8)/dataLen)
        cmd = './PiGen -pub -dataLen %d -pubRate %d:spin -domain 99 -executionTime %d -nic eth0 -pidMultiPubTest 0 -sendQueueSize 50 -qosFile perftest_qos_profiles.xml -numSubscribers 1 -transport UDPv4 -keyed' % (dataLen, pubRate, args.exe_time)
    elif args.platform == 'AMD':
        pubRate = int((args.bandwidth/100)*(AMD_BW*1024*1024/8)/dataLen)
        cmd = './ISISGen -pub -dataLen %d -pubRate %d:spin -domain 99 -executionTime %d -nic em1 -pidMultiPubTest 0 -sendQueueSize 50 -qosFile perftest_qos_profiles.xml -numSubscribers 1 -transport UDPv4 -keyed' % (dataLen, pubRate, args.exe_time)

    print('============== Network Traffic Generator -- <Publisher> ==============')
    print('Note: Please wait one or two miutes before starting runing your own application...')
    os.system(cmd)