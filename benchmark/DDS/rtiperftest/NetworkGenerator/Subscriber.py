#!/usr/bin/python3
import os
import argparse

ARM_BW=95
AMD_BW=950

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--platform', help='Platform', choices=['Arm', 'AMD'])
    parser.add_argument('-d', '--dataLen', help='Data Length(bytes)', default=16384, type=int)

    args = parser.parse_args()

    if args.platform == 'Arm':
        cmd = './PiGen -sub -dataLen %d -domain 99 -transport UDPv4 -numPublishers 1 -sidMultiSubTest 0 -qosFile perftest_qos_profiles.xml -nic eth0 -keyed' % args.dataLen
    elif args.platform == 'AMD':
        cmd = './ISISGen -sub -dataLen %d -domain 99 -transport UDPv4 -numPublishers 1 -sidMultiSubTest 0 -qosFile perftest_qos_profiles.xml -nic em1 -keyed' % args.dataLen

    print('============== Network Traffic Generator -- <Subscriber> ==============')
    print('Note: Please wait one or two miutes before starting runing your own application...')
    os.system(cmd)