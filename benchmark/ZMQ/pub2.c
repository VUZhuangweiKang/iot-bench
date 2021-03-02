//  Weather update server
//  Binds PUB socket to tcp://*:5556
//  Publishes random weather updates

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

int main (void)
{
    //  Prepare our context and publisher
    void *context = zmq_ctx_new ();
    void *publisher = zmq_socket (context, ZMQ_PUB);
    int rc = zmq_bind (publisher, "tcp://*:5556");
    assert (rc == 0);
    struct msg1 s1;
    srandom ((unsigned) time (NULL));
    for (i = 0; i < 50; ++i){
        s1[0].data[i] = rand();
    }
    s1.pubID = "192";

    //  Initialize random number generator
    int j = 0;
    while (j<50) {

        //  Get values that will fool the boss
        s1.sequence = j;
        s1.currentTime = currentTimeInNanoSeconds();
        //  Send message to all subscribers

        s_send (publisher, s1);
        j = j + 1;
    }
    zmq_close (publisher);
    zmq_ctx_destroy (context);
    return 0;
}
