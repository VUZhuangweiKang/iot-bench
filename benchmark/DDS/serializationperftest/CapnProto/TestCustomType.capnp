@0x8704da8ce7e2d5d8;

using Cxx = import "/capnp/c++.capnp";

struct LongSeqTest {
    longSeq @0 :List(Int32);
}

struct DoubleSeqTest {
    doubleSeq @0 :List(Float64);
}

struct StringTest {
    str @0 :Text;
}

struct StringSeqTest {
    stringSeq @0 :List(StringTest);
}

struct ArrayLongSeqTest {
    arrayLongSeq @0 :List(LongSeqTest);
}

struct SeqArrayLongSeqTest {
    seqArrayLongSeq @0 :List(ArrayLongSeqTest);
}

struct TestCustomType {
    testLong @0 :Int32;
    testOctet @1 :List(Int8);
    testLongSeq @2 :LongSeqTest;
    testString @3 :StringTest;
    testStringSeq @4 :StringSeqTest;
    testDoubleSeq @5 :DoubleSeqTest;
    testArrayLongSeq @6 :ArrayLongSeqTest;
    seqArrayLongSeqTest @7 :SeqArrayLongSeqTest;
}