#include "zmq.h"
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

struct opts_struct
{
    char clientid[20];
    char username[10];
    char password[10];
    char address[30];
    char ip[5];
    int port;
    char type[20];
    char topic[30];
    size_t sample_count;
    size_t array_size;
    double interval;
} opts =
        {
                "pi92", "pi92_sks", "123", "iot.eclipse.org", "192", 1883, "none", "test/testing123", 10, 10, 1000
        };


typedef struct measurements{
    size_t sequence;
    long long senderTime;
    long long receiverTime;
    char publisherID[20];
    size_t payloadSize;
}measurement;

static void usage(void) {
    printf("Usage: tutorial_pubsub_mqtt [--url <opc.mqtt://hostname:port>] "
           "[--topic <mqttTopic>] " "[--client_id <Unique identifier of MQTT Client>] " "[--username <Client username>] " "[--password <password>] " "[--sample <Number of samples to receive>]" "[--interval <time in ms>]"
           "  Defaults are:\n"
           "  - Url: iot.eclipse.org\n"
           "  - Topic: customTest\n"
           "  - Samples: 10\n"
           "  - Client ID: pi92\n"
           "  - Username: pi92_sks\n"
           "  - Password: 123\n"
           "  - Interval: 1000\n");

}

long long currentTimeInNanoSeconds() {
    SYSTEM_TIMESPEC tv;
    clock_gettime(CLOCK_REALTIME, &tv);

    long long time =
            (long long)tv.tv_sec * pow(10, 9) + (long long)tv.tv_nsec;
    return time;
}



int main(int argc, char **argv) {
    int argpos;
    for(argpos = 1; argpos < argc; argpos++) {
        if(strcmp(argv[argpos], "--help") == 0) {
            usage();
            return 0;
        }

        if(strcmp(argv[argpos], "--url") == 0) {
            if(argpos + 1 == argc) {
                usage();
                return -1;
            }
            argpos++;
            strncpy(opts.address, argv[argpos], 30);
            continue;
        }

        if(strcmp(argv[argpos], "--topic") == 0) {
            if(argpos + 1 == argc) {
                usage();
                return -1;
            }
            argpos++;
            strncpy(opts.topic, argv[argpos], 30);
            continue;
        }

        if(strcmp(argv[argpos], "--client_id") == 0) {
            if(argpos + 1 == argc) {
                usage();
                return -1;
            }
            argpos++;
            strncpy(opts.clientid, argv[argpos], 20);
            continue;
        }
        if(strcmp(argv[argpos], "--type") == 0) {
            if(argpos + 1 == argc) {
                usage();
                return -1;
            }
            argpos++;
            strncpy(opts.type, argv[argpos], 20);
            continue;
        }

        if(strcmp(argv[argpos], "--username") == 0) {
            if(argpos + 1 == argc) {
                usage();
                return -1;
            }
            argpos++;
            strncpy(opts.username, argv[argpos], 10);
            continue;
        }

        if(strcmp(argv[argpos], "--password") == 0) {
            if(argpos + 1 == argc) {
                usage();
                return -1;
            }
            argpos++;
            strncpy(opts.username, argv[argpos], 10);
            continue;
        }

        if(strcmp(argv[argpos], "--interval") == 0) {
            if(argpos + 1 == argc) {
                usage();
                return -1;
            }
            argpos++;
            if(sscanf(argv[argpos], "%lf", &opts.interval) != 1) {
                usage();
                return -1;
            }
            if(opts.interval < 0) {
                printf("Publication interval too small\n");
                return -1;
            }
            continue;
        }

        if(strcmp(argv[argpos], "--sample") == 0) {
            if(argpos + 1 == argc) {
                usage();
                return -1;
            }
            argpos++;
            if(sscanf(argv[argpos], "%lu", &opts.sample_count) != 1) {
                usage();
                return -1;
            }

            continue;
        }

        if(strcmp(argv[argpos], "--port") == 0) {
            if(argpos + 1 == argc) {
                usage();
                return -1;
            }
            argpos++;
            if(sscanf(argv[argpos], "%d", &opts.port) != 1) {
                usage();
                return -1;
            }

            continue;
        }

        if(strcmp(argv[argpos], "--array_size") == 0) {
            if(argpos + 1 == argc) {
                usage();
                return -1;
            }
            argpos++;
            if(sscanf(argv[argpos], "%lu", &opts.array_size) != 1) {
                usage();
                return -1;
            }
            if(opts.array_size < 1) {
                printf("Array size cannot be zero or less\n");
                return -1;
            }
            continue;
        }

        if(strcmp(argv[argpos], "--ip") == 0) {
            if(argpos + 1 == argc) {
                usage();
                return -1;
            }
            argpos++;
            strncpy(opts.ip, argv[argpos], 5);
            continue;
        }
    }

    void *context = zmq_ctx_new();
    void *socket = zmq_socket(context, ZMQ_SUB);
    int rc = zmq_connect(socket, "tcp://localhost:500");
    assert(rc ==0);
    zmq_setsockopt(socket, ZMQ_SUBSCRIBE, "", 0);

    size_t j = 0;
    msgpack_unpacked msg;
    while(j < opts.sample_count) {
        printf("here\n");
        int size;
        zmq_msg_t in_msg;
        zmq_msg_init(&in_msg);
        zmq_recv(socket, &in_msg, 1000, 0);
        printf("here now\n");
        msgpack_unpacked_init(&msg);

        size = zmq_msg_size(&in_msg);
        msgpack_unpack_next(&msg, zmq_msg_data(&in_msg), size, NULL);
        msgpack_object obj = msg.data;
        msgpack_object_print(stdout, obj);
        printf("\n");

        //int size = zmq_msg_size (&in_msg);
        //memcpy(string, zmq_msg_data(&in_msg), size);
        zmq_msg_close(&in_msg);
        j = j + 1;
    }
    zmq_close(socket);
}
