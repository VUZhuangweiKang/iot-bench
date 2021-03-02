# Latency Test

###### **Settings:**

- Scenarios: 1pub-1sub
- Publishing rate: 200~1000 samples/s
- Message size: 64B, 2KB, 16KB, 32KB
- Bandwidth: 100Mbps
- Execution Time: 90s

###### **Objectives:**

Compare latency of a periodic data stream on the ARM cluster;

###### Run Experiment:

```shell
./perftest_cpp -sub -dataLen <Payload> -sidMultiSubTest 0 -numPublishers <Pub Num> -domain 0 -noPrint -qosFile -transport UDPv4 -cpu -nic em1

./perftest_cpp -pub -dataLen <Payload> -sidMultiPubTest 0 -batchSize 0 -pubRate <Pub Rate>:spin -executionTime 90 -numSublishers <Sub Num> -domain 0 -noPrint -transport UDPv4 -cpu -nic em1
```

###### **Observations(90th** **percentile** **latency):**

- Small Messages(64B / 2KB):
  - MQTT latency is about two times higher than that of DDS and ZMQ;
  - DDS has slightly higher latency than ZMQ;
  - The latency remains flat as the pubRate increases because the reading speed of subscriber can keep up with the sending rate of publisher;
- Large Messages(16KB / 32KB)
  - Latency suddenly increases when subscriber is overwhelmed;
  - MQTT latency remains flat for all pubRate, which implies broker was doing congestion control and publisher was blocked;
  - The standard deviation of ZMQ is much larger than DDS and MQTT, it means messages were piled up on the subscriber side, and high water mark limit was reached.