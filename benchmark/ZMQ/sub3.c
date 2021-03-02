//  Weather update client
//  Connects SUB socket to tcp://localhost:5556
//  Collects weather updates and finds avg temp in zipcode

#include "zhelpers.h"

int main (int argc, char *argv [])
{
    //  Socket to talk to server
    printf ("Collecting updates from weather server…\n");
    void *context = zmq_ctx_new ();
    void *subscriber = zmq_socket (context, ZMQ_SUB);
    int rc = zmq_connect (subscriber, "tcp://localhost:5556");
    assert (rc == 0);

    //  Subscribe to zipcode, default is NYC, 10001
    char *filter = (argc > 1)? argv [1]: "123 ";
    rc = zmq_setsockopt (subscriber, ZMQ_SUBSCRIBE, filter, strlen (filter));
    assert (rc == 0);

    //  Process 100 updates
    int update_nbr;
    long total_temp = 0;
    zmq_msg_t part;
    char *data[1000];
    for (update_nbr = 0; update_nbr < 100; update_nbr++) {
        int64_t more;
        size_t more_size = sizeof more;
        do {
            /* Create an empty ØMQ message to hold the message part */

            int rc = zmq_msg_init (subscriber);
            assert (rc == 0);
            /* Block until a message is available to be received from socket */
            rc = zmq_recv (subscriber, &part, sizeof(part), 0);
            assert (rc == 0);
            /* Determine if more message parts are to follow */
            rc = zmq_getsockopt (subscriber, ZMQ_RCVMORE, &more, &more_size);
            assert (rc == 0);
            zmq_msg_close (&part); } while (more);

        memcpy(data, zmq_msg_data(&part), sizeof(data));


        // char *string = s_recv (subscriber);
        // int zipcode, temperature;
        // long zipcode2, temperature2;
        // long long sentTime;
        // long sentTime2;
        // sscanf (string, "%d %d %lld %ld %ld %ld", &zipcode, &temperature, &sentTime, &zipcode2, &temperature2, &sentTime2);
        // printf("%d %d %lld %ld %ld %ld\n", zipcode, temperature, sentTime, zipcode2, temperature2, sentTime2);
        // free (string);
    }
    zmq_close (subscriber);
    zmq_ctx_destroy (context);
    return 0;
}
