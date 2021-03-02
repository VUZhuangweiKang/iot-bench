//  Weather update client
//  Connects SUB socket to tcp://localhost:5556
//  Collects weather updates and finds avg temp in zipcode

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
} opts =
        {
                1, 100, 50
        };

typedef struct measurements{
    int pubID;
    size_t sequence;
    double senderTime;
    double receiverTime;
}measurement;

measurement *measure;

size_t message_count = 0;

void flush_msg()
{
    if (message_count==0) return;

    char filename[50];
    snprintf(filename,50,"perf_log_zmq_%u.csv",opts.clientid);
    printf("writing to file %s\n",filename);

    FILE *f = fopen(filename, "w");

    size_t j;
    for (j = 0; j < message_count; j++){
        //printf("%ld,%s,%lld,%lld,%ld\n", measure[j].sequence, measure[j].publisherID, measure[j].senderTime, measure[j].receiverTime, measure[j].payloadSize);
        fprintf(f,"%u,%u,%lf,%lf\n", measure[j].sequence, measure[j].pubID, measure[j].senderTime, measure[j].receiverTime);
    }
    fclose(f);
}

static void usage(void) {
    printf("Usage: subscriber [--url <iot.eclipse.org>] "
           "[--topic <mqttTopic>] "  "[--sample <Number of samples to receive>]"
           "  Defaults are:\n"
           "  - Url: iot.eclipse.org\n"
           "  - Topic: test/testing123\n"
           "  - Samples: 10\n");
}

static void stopHandler(int sign) {
    printf("Received Ctrl-C\n");
    flush_msg();
}

long long currentTimeInNanoSeconds() {
    SYSTEM_TIMESPEC tv;
    clock_gettime(CLOCK_REALTIME, &tv);

    long long time =
            (long long)tv.tv_sec * pow(10, 9) + (long long)tv.tv_nsec;
    return time;
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
          if(sscanf(argv[argpos], "%u", &opts.clientid) != 1) {
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
          if(sscanf(argv[argpos], "%u", &opts.array_size) != 1) {
              usage();
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
          if(sscanf(argv[argpos], "%u", &opts.sample_count) != 1) {
              usage();
              return -1;
          }

          continue;
      }
  }

  //  Socket to talk to server
  printf ("Collecting data…\n");
  void *context = zmq_ctx_new ();
  void *subscriber = zmq_socket (context, ZMQ_SUB);
  int rc = zmq_connect (subscriber, "tcp://192.168.88.87:5555");
  assert (rc == 0);

  //int timeout = 10000;
  rc = zmq_setsockopt (subscriber, ZMQ_SUBSCRIBE, "", 0);
  //rc = zmq_setsockopt (subscriber, ZMQ_RCVTIMEO, &timeout, sizeof(int));
  assert (rc == 0);
  measure = (measurement *)malloc(2*opts.sample_count*sizeof(measurement));
  double lastTime = currentTimeInNanoSeconds();
  //  Process 100 updates
  int update_nbr;
  for (update_nbr = 0; update_nbr < opts.sample_count; update_nbr++) {

    zmq_msg_t msg;
    rc = zmq_msg_init (&msg);
    assert (rc == 0);

    /* Block until a message is available to be received from socket */
    rc = zmq_msg_recv (&msg, subscriber, 0);
    printf("hello %u\n", update_nbr); 
    double recvTime = currentTimeInNanoSeconds();
    lastTime = recvTime;
    //if (rc == -1){
      //flush_msg();
      //update_nbr = opts.sample_count;
    //}
    assert (rc != -1);

    msgpack_unpacked unpacked_msg;
    msgpack_unpacked_init(&unpacked_msg);
    void *message_copy = malloc(zmq_msg_size(&msg));
    memcpy(message_copy, zmq_msg_data(&msg), zmq_msg_size(&msg));
    bool success = msgpack_unpack_next(&unpacked_msg, (const char *)message_copy, zmq_msg_size(&msg), NULL);
    msgpack_object root = unpacked_msg.data;
    assert(success);

    int seq = root.via.array.ptr[0].via.u64;
    int Id = root.via.array.ptr[1].via.u64;
    double sendTime = root.via.array.ptr[opts.array_size+2].via.f64;

    measure[update_nbr].senderTime = sendTime;
    measure[update_nbr].receiverTime = recvTime;
    measure[update_nbr].sequence = seq;
    measure[update_nbr].pubID = Id;

    //printf("%d %lf\n", seq, sendTime);
    message_count = message_count + 1;

    msgpack_unpacked_destroy(&unpacked_msg);
    zmq_msg_close(&msg);
    free(message_copy);
  }
  if (message_count == opts.sample_count){
    flush_msg();
  }
  //flush_msg();
  free(measure);
  zmq_close (subscriber);
  zmq_ctx_destroy (context);
  return 0;
}
