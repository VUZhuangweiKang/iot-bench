#!/bin/bash
for IF in em1 em2 p1p1 virbr0 virbr0-nic
do
    sudo tc qdisc change dev $IF root tbf rate 100mbit latency 50ms burst 1000kb
done
