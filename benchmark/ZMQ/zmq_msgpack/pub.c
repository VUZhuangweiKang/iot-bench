   //  Binds PUB socket to tcp://*:5556
   //  Publishes random weather updates

#include "zhelpers.h"
#include "msgpack.h"
#include <unistd.h>
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

#define SYSTEM_TIMESPEC struct timespec
int stop == 0;

struct opts_struct
{
    size_t clientid;
    size_t sample_count;
    size_t array_size;
    float interval;
} opts =
        {
                0, 10, 10, 1000
        };

long long currentTimeInNanoSeconds() {
    SYSTEM_TIMESPEC tv;
    clock_gettime(CLOCK_REALTIME, &tv);

    long long time =
            (long long)tv.tv_sec * pow(10, 9) + (long long)tv.tv_nsec;
    return time;
}

static void stopHandler(int sign) {
    printf("Received Ctrl-C\n");
    stop  = 1;
}

static void usage(void) {
    printf("Usage: ./pub "
           "[--topic <mqttTopic>] " "[--client_id <Unique identifier of MQTT Client>] " "[--sample <Number of samples to receive>]" "[--interval <time in ms>]"
           "  Defaults are:\n"
           "  - Samples: 10\n"
           "  - Client ID: (int)\n"
           "  - Interval: 1000\n");

}

void timespec_add_us(struct timespec *t, uint64_t delta)
{
    t->tv_nsec=t->tv_nsec+(1000*delta);
    if(t->tv_nsec>=1000000000)
    {
        t->tv_sec=t->tv_sec+(t->tv_nsec/1000000000);
        t->tv_nsec=t->tv_nsec%1000000000;
    }
}

int main (int argc, char **argv)
{
  signal(SIGINT, stopHandler);
  signal(SIGTERM, stopHandler);

  /* Parse arguments */
  int argpos;
  for(argpos = 1; argpos < argc; argpos++) {
      if(strcmp(argv[argpos], "--help") == 0) {
          usage();
          return 0;
      }

      if(strcmp(argv[argpos], "--client_id") == 0) {
          if(argpos + 1 == argc) {
              usage();
              return -1;
          }
          argpos++;
          if(sscanf(argv[argpos], "%lu", &opts.clientid) != 1) {
              usage();
              return -1;
          }
          continue;
      }

      if(strcmp(argv[argpos], "--interval") == 0) {
          if(argpos + 1 == argc) {
              usage();
              return -1;
          }
          argpos++;
          if(sscanf(argv[argpos], "%f", &opts.interval) != 1) {
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
  }

  //  Prepare our context and publisher
  void *context = zmq_ctx_new ();
  void *publisher = zmq_socket (context, ZMQ_PUB);
  int rc = zmq_bind (publisher, "tcp://*:5555");
  assert (rc == 0);
  msgpack_sbuffer* buffer;
  msgpack_packer* pk;
  sleep(5);

  //  Initialize random number generator
  srandom ((unsigned) time (NULL));
  size_t i = 0;
  struct timespec r;
  int period = opts.interval*1000;
  clock_gettime(CLOCK_REALTIME, &r);
  timespec_add_us(&r, period);

  while (i < opts.sample_count) {
    buffer = msgpack_sbuffer_new();
    pk = msgpack_packer_new(buffer, msgpack_sbuffer_write);
    msgpack_pack_array(pk, 3+opts.array_size);
    msgpack_pack_uint64(pk, i);
    msgpack_pack_uint64(pk, opts.clientid);
    int j;
    for (j=0;j<opts.array_size;j++){
      msgpack_pack_uint64(pk, rand());
    }

    msgpack_pack_double(pk, currentTimeInNanoSeconds());
    msgpack_pack_uint64(pk, 5);
    msgpack_pack_uint64(pk, 5);
    zmq_send(publisher, buffer->data, buffer->size, 0);
    printf("Size: %lu\n", buffer->size);
    // sleep (.0001);
    clock_nanosleep(CLOCK_REALTIME, TIMER_ABSTIME, &r, NULL);
    timespec_add_us(&r, period);
    msgpack_packer_free(pk);
    msgpack_sbuffer_free(buffer);
    i = i+1;
  }
  zmq_close (publisher);
  zmq_ctx_destroy (context);
  return 0;
}
