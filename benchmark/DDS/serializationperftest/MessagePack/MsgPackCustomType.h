//
// Created by 康壮伟 on 2019-10-07.
//

#include "../utl.cpp"
#include <msgpack.hpp>

#ifndef MSGPACK_CUSTOMTYPE_H
#define MSGPACK_CUSTOMTYPE_H

typedef unsigned char octet;

typedef struct LongSeqTest {
    int32_t long_seq[SIZE_TEST_SEQ];
    MSGPACK_DEFINE(long_seq);
}LongSeqTest;

typedef struct DoubleSeqTest {
    double double_seq[SIZE_TEST_SEQ];
    MSGPACK_DEFINE(double_seq);
}DoubleSeqTest;

typedef struct StringTest {
    char str[SIZE_TEST_STR];
    MSGPACK_DEFINE(str);
}StringTest;

typedef struct StringSeqTest {
    StringTest string_seq[SIZE_TEST_SEQ];
    MSGPACK_DEFINE(string_seq);
}StringSeqTest;

typedef struct ArrayLongSeqTest {
    LongSeqTest array_long_seq[SIZE_TEST_ARRAY_SEQ];
    MSGPACK_DEFINE(array_long_seq);
}ArrayLongSeqTest;

typedef struct SeqArrayLongSeqTest {
    ArrayLongSeqTest seq_array_long_seq[SIZE_TEST_SEQ_ARRAY_SEQ];
    MSGPACK_DEFINE(seq_array_long_seq);
}SeqArrayLongSeqTest;

typedef struct TestCustomType {
    int32_t test_long;
    octet test_octet[SIZE_OCTET_ARRAY];
    LongSeqTest test_long_seq;
    StringTest test_string;
    StringSeqTest test_string_seq;
    DoubleSeqTest test_double_seq;
    ArrayLongSeqTest test_array_long_seq;
    SeqArrayLongSeqTest seq_array_long_seq_test;

    MSGPACK_DEFINE(test_long, test_octet, test_long_seq, test_string, test_string_seq, test_double_seq, test_array_long_seq, seq_array_long_seq_test);

}TestCustomType;


#endif //MSGPACK_CUSTOMTYPE_H
