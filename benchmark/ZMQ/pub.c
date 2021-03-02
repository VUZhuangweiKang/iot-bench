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


struct msg1 {
    char pubID[20];
    size_t sequence;
    long long currentTime;
    long data[1];
};

void free_msgpack_msg(void *data, void *buffer) {
    msgpack_sbuffer_free((msgpack_sbuffer*)buffer);
}

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
    struct msg1 s2;
    strncpy(s2.pubID, opts.clientid, sizeof(opts.clientid));;
    
    void *context = zmq_init(1);
    void *socket = zmq_socket(context, ZMQ_PUB);
    zmq_connect(socket, "tcp://127.0.0.1:500");
    sleep(1);
    size_t j = 0;
    srand(time(0));
    //char message[1000] = "testing\n";
    while(j < opts.sample_count) {
        s2.sequence = j;
        msgpack_sbuffer *buffer = msgpack_sbuffer_new();
        msgpack_sbuffer_init(buffer);
        msgpack_packer* pk = msgpack_packer_new(buffer, msgpack_sbuffer_write); 
        /// pack
        
        msgpack_pack_int(pk, s2.sequence);
        size_t k;
        msgpack_pack_array(pk, 3+opts.array_size);
        for(k=0;k<opts.array_size;k++){
            msgpack_pack_uint32(pk, rand());
        }
        msgpack_pack_str(pk, 20);
        msgpack_pack_str_body(pk, s2.pubID, 20);
        msgpack_pack_uint64(pk, currentTimeInNanoSeconds());
        msgpack_packer_free(pk);

        zmq_msg_t msg;
        zmq_msg_init_data(&msg, buffer->data, buffer->size, free_msgpack_msg,buffer);
        zmq_send(socket, &msg, buffer->size, 0);
        printf("Sent message (%ld) with size (%ld)\n", j, buffer->size);
        j = j + 1;
        sleep(2);
        //zmq_msg_t out_msg;
        //zmq_msg_init_size(&out_msg, strlen(message));
        //memcpy(zmq_msg_data(&out_msg), message, strlen(message));
        //zmq_send(socket, &out_msg, 0);
        //zmq_msg_close(&out_msg);
        //sleep(1);
    }
}
