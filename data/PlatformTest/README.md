# Platform Test

###### **Settings:**

- Scenarios: 1pub-1sub
- Publishing rate: unlimited
- Bandwidth: 100Mbps
- CPU: 1 core was used

###### **Objective:**

Evaluate the impact of platform hardware to application throughput.       

###### Platform Configurations

| Hardware  | Raspberry Pi Cluster                                         | BeagleBone Blacks Cluster                                    |
| --------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| CPU       | 1.2GHz / 4 Cores                                             | 1GHz / 1 Cores                                               |
| RAM       | 1GB                                                          | 512MB                                                        |
| Bandwidth | <100Mbps                                                     | <100Mbps                                                     |
| Router    | MikroTik CCR1036-12G-4S 12x 10/100/1000 Ethernet ports LAN Ports, 1.2GHz CPU | Microtik Router Board, five 1Gbps ports/ five 100mbps ports, 2.4 GHz CPU |

###### Observations:

- For DDS, the throughput of application has similar trend, application relatively poor performance on the BBB cluster due to the limitation of CPU;
- In the ZMQ experiment, application has higher throughput on the BBB cluster when message size is smaller than 256B because the CPU clock speed of the router in BBB cluster is faster; 
- As we keep increase the payload, publisher CPU becomes the primary bottleneck again.