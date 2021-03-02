#!/usr/bin/python3
import pandas as pd

if __name__ == "__main__":
    apps = [(1, 1), (1, 7), (7, 1), (3, 4)]
    platforms = ['Armv7l', 'AMD64']

    multicast = [False, True]
    turboMode = [False, True]
    autoThrottle = [False, True]
    sendQueueSize = [50, 100]
    useReadThread = [False, True]

    """
    values are determined by SpinCheck
    if AutoThrottle is enabled, ignore spin
    0: fast pubRate
    1000/5000: medium pubRate
    10000/50000: slow pubRate
    """
    spin = {
        'Armv7l': [10000, 1000, 0, 'auto'],
        'AMD64': [50000, 5000, 0, 'auto']
    }

    """
    0: DDS_VOLATILE_DURABILITY_QOS:
        Do not save or deliver old DDS samples.
    2: DDS_TRANSIENT_DURABILITY_QOS:
        Save and deliver old DDS samples using a memory-based service.
    """
    durability = [0, 2]

    # ================================================
    """
    If durability = 0, history QoS is ignored
    """
    history = ['all', 50]

    # The following QoS settings must be set in XML file
    heartbeat = ['slow', 'normal', 'fast']
    
    """
    0: unlimited latency budget
    10000000: 10 milliseconds latency budget
    """
    latency_budgets = [0, 10000000]

    # =================================================
    latencyTest = [True, False]
    head = ['Platform', 'Publisher', 'Subscriber', 'Multicast', 'EnableTurboMode', 'EnableAutoThrottle',
            'SendQueueSize', 'UseReadThread', 'Spin', 'Durability', 'History', 'Heartbeat', 'LatencyBudget', 'LatencyTest']
    results = []

    qos = [multicast, turboMode, autoThrottle, sendQueueSize, useReadThread, spin, durability, history, heartbeat, latency_budgets]

    ##############################################################
    # QoS:
    # Multicast, TurboMode, AutoThrottle, SendQueueSize, UseReadThread, Spin, Durability, History, Heartbeat, LatencyBudget
    default = [multicast[0], turboMode[0], autoThrottle[0], sendQueueSize[0], useReadThread[0], spin['Armv7l'][2], durability[0], history[0], heartbeat[1], latency_budgets[0]]

    for app in apps:
        for platform in platforms:
            for test in latencyTest:
                for i, q in enumerate(qos):
                    if i == 5:
                        q = q[platform]
                    for val in q:
                        temp = default[:]
                        temp[i] = val
                        # insert pub/sub number
                        temp.insert(0, app[0])
                        temp.insert(1, app[1])

                        # insert test info
                        temp.append(test)
                        temp.insert(0, platform)
                        results.append(temp)
    
    real_result = []
    # if durability = 0, history is ignored
    for i, item in enumerate(results[:]):
        # if auto-throttle is enabled, spin is automatically determined
        if item[5]:
            item[8] = 'auto'
        # if history=50, durability=2
        if item[10] == 50:
            item[9] == 2
        if (item in real_result) or ((not item[5]) and item[8] == 'auto'):
            continue
        real_result.append(item)

    df = pd.DataFrame(real_result, columns=head, index=None)
    df.to_csv('./NewExpSchedule.csv', index=False)
