//  Weather update client
//  Connects SUB socket to tcp://localhost:5556
//  Collects weather updates and finds avg temp in zipcode

#include "zhelpers.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <msgpack.h>
#include <signal.h>
#include <memory.h>
#include <sys/time.h>
#include <stdint.h>
#include <ifaddrs.h>
#include <time.h>
#include <sys/timeb.h>
#include <math.h>
#include <unistd.h>

#define SYSTEM_TIMESPEC struct timespec

struct msg1 {
    char pubID[20];
    size_t sequence;
    long long currentTime;
    long data[1];
};

long long currentTimeInNanoSeconds() {
    SYSTEM_TIMESPEC tv;
    clock_gettime(CLOCK_REALTIME, &tv);

    long long time =
            (long long)tv.tv_sec * pow(10, 9) + (long long)tv.tv_nsec;
    return time;
}

int main (int argc, char *argv [])
{
    //  Socket to talk to server
    printf ("Collecting updates from weather server…\n");
    void *context = zmq_ctx_new ();
    void *subscriber = zmq_socket (context, ZMQ_SUB);
    int rc = zmq_connect (subscriber, "tcp://localhost:5556");
    assert (rc == 0);

    //  Subscribe to zipcode, default is NYC, 10001
    rc = zmq_setsockopt (subscriber, ZMQ_SUBSCRIBE, "", 0);
    assert (rc == 0);

    //  Process 100 updates
    int i;
    long long recvTime[50];
    long long sendTime[50];
    for (i = 0; i < 50; i++) {
        struct msg1 string = s_recv(subscriber);
        size_t num = string.sequence;
        printf("received message %ld", num);
        recvTime[i] = currentTimeInNanoSeconds();
        sendTime[i] = string.currentTime;

        free (string);
    }


    zmq_close (subscriber);
    zmq_ctx_destroy (context);
    return 0;
}
