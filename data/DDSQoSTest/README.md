# DDS QoS Test

###### **Settings:** 

- Scenarios: 1pub-1sub
- Publishing rate: unlimited
- Bandwidth: 100Mbps
- Testbed: ARM
- Execution Time: 90s

###### **Objective:** 

Evaluate the effects of several QoS settings in DDS on application performance;

###### Run Experiment:

```shell
./perftest_cpp -sub -dataLen <Payload> -sidMultiSubTest 0 -numPublishers 1 -domain 0 -noPrint -transport UDPv4 -cpu -nic em1

./perftest_cpp -pub -dataLen <Payload> -sidMultiPubTest 0 -batchSize 0 -pubRate <Pub Rate>:spin -executionTime 90 -numSublishers 1 -domain 0 -noPrint -transport UDPv4 -cpu -nic em1 < -enableTurboMode / -enableAutoThrottle / -multicast / -qosFile perftest_qos_profiles_slow_hb.xml >
```

###### **Observations:**

- 1pub-1sub
  - Throughput improves as packets size increases and gradually converges to the maximum bandwidth.
  - The TurboMode mode improves throughput for small messages;
  - The AutoThrottle mode cuts down throughput, but contributes less to latency, it also leads to higher CPU utilization.
- 1pub-7sub
  - Multicast effectively improves application performance;
  - The throughput of Multicast does not converge to the physical bandwidth as payload increases due to the limitation of switch;
  - The AutoThrottle is designed to reduce latency by auto-adjusting send window size and writing rate. But results show that it performs not as good as expected;
  - The TurboMode improves throughput for small packets because of its internal intelligent batching algorithm;
  - Latency is reduced if we slow down the heartbeat frequency.

