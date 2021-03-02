# Serialization Test

###### **Setting:**

Serialize a 14KB message that involves multiple data types on the AMD cluster for 1000 times.

###### **Objective:**

Compare efficiency of several common used (de)serialization methods, including CDR, Cap’n Proto, Protobuffer, and MessagePack;

###### Data Structure of the Message:

```c++
const long SIZE_TEST_STR = 16;
const long SIZE_TEST_SEQ = 128;
const long SIZE_TEST_ARRAY_SEQ = 4;
const long SIZE_TEST_SEQ_ARRAY_SEQ = 4;
const long SIZE_OCTET_ARRAY = 360;

struct LongSeqTest {
    sequence<long, SIZE_TEST_SEQ> test_long_seq;
};//@Extensibility FINAL_EXTENSIBILITY

struct DoubleSeqTest {
    sequence<double, SIZE_TEST_SEQ> test_double_seq;
};//@Extensibility FINAL_EXTENSIBILITY

struct StringTest {
    char test_string[SIZE_TEST_STR];
};//@Extensibility FINAL_EXTENSIBILITY

struct StringSeqTest {
    sequence<StringTest, SIZE_TEST_SEQ> test_string_seq;
};//@Extensibility FINAL_EXTENSIBILITY

struct ArrayLongSeqTest {
    LongSeqTest test_array_long_seq[SIZE_TEST_ARRAY_SEQ];
};//@Extensibility FINAL_EXTENSIBILITY

struct SeqArrayLongSeqTest {
    sequence<ArrayLongSeqTest, SIZE_TEST_SEQ_ARRAY_SEQ> seq_array_long_seq_test;
};//@Extensibility FINAL_EXTENSIBILITY

struct TestCustomType {
    long test_long;
    octet test_octet[SIZE_OCTET_ARRAY];
    LongSeqTest test_long_seq;
    StringTest test_string;
    StringSeqTest test_string_seq;
    DoubleSeqTest test_double_seq;
    ArrayLongSeqTest test_array_long_seq;
    SeqArrayLongSeqTest seq_array_long_seq_test;
};//@Extensibility FINAL_EXTENSIBILITY
```

###### **Observations:**

CDR has the best performance, followed by Cap’n Proto, Protobuffer, and MessagePack.

