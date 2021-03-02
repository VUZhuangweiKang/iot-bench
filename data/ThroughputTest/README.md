# Throughput Test

###### **Settings:**

- Scenarios: 1pub-1sub & 1pub-7sub
- Publishing rate: unlimited
- Bandwidth: 100Mbps
- Execution Time: 90s

###### **Objective:**

Compare the maximum throughput with unlimited pubRate on the ARM cluster.

###### Run Experiment:

```shell
./perftest_cpp -sub -dataLen <Payload> -sidMultiSubTest <Sub ID> -numPublishers <pub num> -domain 0 -noPrint -transport UDPv4 -cpu -nic em1

./perftest_cpp -pub -dataLen <Payload> -sidMultiPubTest <Pub ID> -pubRate <Pub Rate>:spin -batchSize 0 -executionTime 90 -numSublishers <Sub Num> -domain 0 -noPrint -transport UDPv4 -cpu -nic em1
```

###### Observations:

- 1pub-1sub
  - ZMQ has higher throughput than DDS if packet is smaller than 1KB;
  - DDS performs more reliably than ZMQ and MQTT for large messages;
  - Throughput of MQTT slows down as packet size increase;

- 1pub-7sub
  - The throughput is predictably cut down to 1/7th of the original bandwidth.
  - ZMQ consistently has the highest throughput;
  - Similar throughput for large messages, such as 16KB~32KB.