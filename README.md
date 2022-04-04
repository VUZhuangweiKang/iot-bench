# IoT-Bench

This repository is for the paper: [A Study of Publish/Subscribe Middleware Under Different IoT Traffic Conditions](https://dl.acm.org/doi/abs/10.1145/3429881.3430109), acepted by *2020 The International Workshop on Middleware and Applications for the Internet of Things (M4IoT)*.

## Abstract from the M4IoT'20 Paper

Publish/Subscribe (pub/sub) semantics are critical for IoT applications due to their loosely coupled nature. Although OMG DDS, MQTT, and ZeroMQ are mature pub/sub solutions used for IoT, prior studies show that their performance varies significantly under different load conditions and QoS configurations, which makes middleware selection and configuration decisions hard.  Moreover, the load conditions and role of QoS settings in prior comparison studies are not comprehensive and well-documented. To address these limitations, we (1) propose a set of performance-related properties for pub/sub middleware and investigate their support in DDS, MQTT, and ZeroMQ; (2) perform systematic experiments under three representative, lab-based real-world IoT use cases; and (3) improve DDS performance by applying three of our proposed QoS properties. Empirical results show that DDS has the most thorough QoS support, and more reliable performance in most scenarios. In addition, its Multicast, TurboMode, and AutoThrottle QoS policies can effectively improve DDS performance in terms of throughput and latency. 
