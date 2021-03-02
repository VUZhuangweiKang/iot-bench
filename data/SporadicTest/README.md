# Bursty Sporadic Interference Test

###### **Settings:** 

- Periodic Dataflow(PDF):
  - Message size: 64 ~ 32768 bytes(increases by powers of 2)
  - Scenario: 1pub-1sub
  - Publishing Rate: 25Mbps
  - Testbed: ARM
  - Execution Time: 90s

- Sporadic Dataflow(SDF):
  - Message size: 2MB
  - Scenario: 1pub-1sub
  - Publishing Rate: unlimited
  - Testbed: ARM
  - Execution Time: 10s

###### **Objective:** 

Explore the impact of burst MB-level sporadic data flow on the latency of a periodic data flow. 

###### Run Experiment:

```shell
./perftest_cpp -sub -dataLen 2097152 -domain 9 -transport UDPv4 -numPublishers 1 -sidMultiSubTest 0 -nic eth0

./perftest_cpp -pub -dataLen 2097152 -pubRate 0:spin -domain 9 -nic eth0 -pidMultiPubTest 0 -numSubscribers 1 -transport UDPv4  -executionTime 10
```

###### **Observations:**

- The latency of MQTT has extremely higher standard deviation than that of DDS and MQTT, which implies it is more sensitive to the burst stream.
- DDS is relatively better to handle this case than ZMQ.

