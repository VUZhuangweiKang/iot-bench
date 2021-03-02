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

struct opts_struct
{
    size_t clientid;
    size_t sample_count;
    size_t array_size;
    size_t type;
    float interval;
} opts =
        {
                0, 10, 10, 0, 1000
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

      if(strcmp(argv[argpos], "--type") == 0) {
          if(argpos + 1 == argc) {
              usage();
              return -1;
          }
          argpos++;
          if(sscanf(argv[argpos], "%lu", &opts.type) != 1) {
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
  long long start[opts.sample_count];
  long long end[opts.sample_count];
  char dataType[10];
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
    if (opts.type == 0) {
      msgpack_pack_uint64(pk, i);
      msgpack_pack_uint64(pk, opts.clientid);
      int j;
      start[i] = currentTimeInNanoSeconds();
      for (j=0;j<opts.array_size;j++){
        msgpack_pack_short(pk, (short)rand());
      }
      end[i] = currentTimeInNanoSeconds();
      msgpack_pack_double(pk, currentTimeInNanoSeconds());
    }
    else if(opts.type == 1){
      msgpack_pack_uint64(pk, i);
      msgpack_pack_uint64(pk, opts.clientid);
      int j;
      start[i] = currentTimeInNanoSeconds();
      for (j=0;j<opts.array_size;j++){
        msgpack_pack_long(pk, (long)rand());
      }
      end[i] = currentTimeInNanoSeconds();
      msgpack_pack_double(pk, currentTimeInNanoSeconds());
    }
    else if(opts.type == 2){
      msgpack_pack_uint64(pk, i);
      msgpack_pack_uint64(pk, opts.clientid);
      int j;
      start[i] = currentTimeInNanoSeconds();
      for (j=0;j<opts.array_size;j++){
        msgpack_pack_float(pk, (float)rand());
      }
      end[i] = currentTimeInNanoSeconds();
      msgpack_pack_double(pk, currentTimeInNanoSeconds());
    }
    else if(opts.type == 3){
      msgpack_pack_uint64(pk, i);
      msgpack_pack_uint64(pk, opts.clientid);
      int j;
      start[i] = currentTimeInNanoSeconds();
      for (j=0;j<opts.array_size;j++){
        msgpack_pack_double(pk, (double)rand());
      }
      end[i] = currentTimeInNanoSeconds();
      msgpack_pack_double(pk, currentTimeInNanoSeconds());
    }
    else if(opts.type == 4) {
      msgpack_pack_uint64(pk, i);
      msgpack_pack_uint64(pk, opts.clientid);
      int j;
      start[i] = currentTimeInNanoSeconds();
      for (j=0;j<opts.array_size;j++){
        msgpack_pack_str(pk, 3);
        msgpack_pack_str_body(pk, "abc", 3);
      }
      end[i] = currentTimeInNanoSeconds();
      msgpack_pack_double(pk, currentTimeInNanoSeconds());
    }

    zmq_send(publisher, buffer->data, buffer->size, 0);
    printf("Size: %lu\n", buffer->size);

    clock_nanosleep(CLOCK_REALTIME, TIMER_ABSTIME, &r, NULL);
    timespec_add_us(&r, period);
    msgpack_packer_free(pk);
    msgpack_sbuffer_free(buffer);
    i = i+1;
  }
  zmq_close (publisher);
  zmq_ctx_destroy (context);

  char filename[50];
  snprintf(filename,50,"serialize_%lu.csv",opts.type);
  printf("writing to file %s\n",filename);

  FILE *f = fopen(filename, "w");

  size_t j;
  for (j = 0; j < opts.sample_count; j++){
      fprintf(f,"%lu,%lu,%lld,%lld\n", j, opts.type, start[j], end[j]);
  }
  fclose(f);
  return 0;
}
