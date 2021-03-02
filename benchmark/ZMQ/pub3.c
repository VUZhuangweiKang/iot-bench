//  Weather update server
//  Binds PUB socket to tcp://*:5556
//  Publishes random weather updates

#include "zhelpers.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
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

    //  Initialize random number generator
    srandom ((unsigned) time (NULL));
    int seq = 0;
    while (1) {

        //  Get values that will fool the boss
        //int zipcode, temperature, relhumidity;
        //zipcode     = randof (100000);
        //temperature = randof (215) - 80;
        long long time = currentTimeInNanoSeconds();
        long i = 4;
        //  Send message to all subscribers
        char update [50];
        sprintf (update, "123 %d %lld", seq, time);
        printf("%s\n", update);
        s_sendmore (publisher, update);
        s_send_int(publisher, i);
        seq = seq+1;
    }
    zmq_close (publisher);
    zmq_ctx_destroy (context);
    return 0;
}
