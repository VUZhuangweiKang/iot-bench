#!/usr/bin/python3
import time

def perftest_spin(spinCount):
    for spin in range(spinCount):
        a = 3
        b = 1
        c = (a/b)*spin

def get_spin_per_microsecond(precision=100):
    # Same default values used by DDS
    spinCount = 200000
    clockCalculationLoopCountMax = 100

    usec = 0
    iterations = 0

    while usec < precision and iterations < clockCalculationLoopCountMax:
        # get current time in microseconds
        usec = int(time.time() * 1e6)
        # Initial time
        perftest_spin(spinCount * iterations)
        usec = int(time.time() * 1e6) - usec
        # Final time
        iterations += 1
        
    return (iterations * spinCount) / usec

if __name__ == '__main__':
	rlt = get_spin_per_microsecond()
	print(rlt)



./perftest_cpp -sub -dataLen 64 -sidMultiSubTest 0 -numPublishers 2 -domain 0 -noPrint -qosFile perftest_qos_profiles.xml -transport UDPv4 -cpu -nic em1
./perftest_cpp -pub -pubRate 486400:spin -dataLen 64 -pidMultiPubTest 0 -executionTime 60 -numSubscribers 1 -sendQueueSize 50 -domain 0 -noPrint -qosFile perftest_qos_profiles.xml -transport UDPv4 -cpu -nic em1
./perftest_cpp -pub -dataLen 2097152 -sleep 30 -pidMultiPubTest 1 -executionTime 10 -numSubscribers 1 -sendQueueSize 50 -domain 0 -noPrint -qosFile perftest_qos_profiles.xml -transport UDPv4 -cpu -nic em1




./perftest_cpp -sub -dataLen 64 -sidMultiSubTest 0 -numPublishers 1 -domain 0 -noPrint -qosFile perftest_qos_profiles.xml -transport UDPv4 -cpu -nic em1
./perftest_cpp -sub -dataLen 2097152 -sidMultiSubTest 0 -numPublishers 1 -domain 0 -noPrint -qosFile perftest_qos_profiles.xml -transport UDPv4 -cpu -nic em1
./perftest_cpp -pub -pubRate 97:spin -dataLen 64 -pidMultiPubTest 0 -executionTime 60 -numSubscribers 1 -sendQueueSize 50 -domain 0 -noPrint -qosFile perftest_qos_profiles.xml -transport UDPv4 -cpu -nic em1
./perftest_cpp -pub -dataLen 2097152 -sleep 10 -pidMultiPubTest 0 -executionTime 60 -numSubscribers 1 -sendQueueSize 50 -domain 0 -noPrint -qosFile perftest_qos_profiles.xml -transport UDPv4 -cpu -nic em1