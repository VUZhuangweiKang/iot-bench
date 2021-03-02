//
// Created by zhuangwei on 10/11/19.
//

#include "TestCustomType.capnp.h"
#include "../utl.cpp"
#include "TestPipe.cpp"

using namespace capnp;

TestCustomType::Builder initStruct(MallocMessageBuilder &message, int32_t key) {
    TestCustomType::Builder customType = message.initRoot<TestCustomType>();

    List<int8_t >::Builder octets = customType.initTestOctet(SIZE_OCTET_ARRAY);
    for (int i = 0; i < SIZE_OCTET_ARRAY; ++i)
        octets.set(i, (int8_t)key);

    customType.initTestString().initStr(SIZE_TEST_STR);
    customType.getTestString().setStr("Hello World!");

    List<int32_t>::Builder long_seq = customType.initTestLongSeq().initLongSeq(SIZE_TEST_SEQ);
    List<StringTest>::Builder str_seq = customType.initTestStringSeq().initStringSeq(SIZE_TEST_SEQ);
    List<double_t>::Builder double_seq = customType.initTestDoubleSeq().initDoubleSeq(SIZE_TEST_SEQ);

    for (int j = 0; j < SIZE_TEST_SEQ; ++j) {
        long_seq.set(j, (int32_t)j);
        StringTest::Builder str = str_seq[j];
        str.setStr(customType.getTestString().getStr());
        double_seq.set(j, (double_t)j);
    }

    List<LongSeqTest>::Builder array_long_seq = customType.initTestArrayLongSeq().initArrayLongSeq(SIZE_TEST_ARRAY_SEQ);
    for (int k = 0; k < SIZE_TEST_ARRAY_SEQ; ++k) {
        LongSeqTest::Builder long_seq_ = array_long_seq[k];
        long_seq_.setLongSeq(long_seq);
    }

    List<ArrayLongSeqTest>::Builder seq_array_long_seq_builder = customType.initSeqArrayLongSeqTest().initSeqArrayLongSeq(SIZE_TEST_SEQ_ARRAY_SEQ);
    for (int l = 0; l < SIZE_TEST_SEQ_ARRAY_SEQ; ++l) {
        ArrayLongSeqTest::Builder array_long_seq_ = seq_array_long_seq_builder[l];
        array_long_seq_.setArrayLongSeq(array_long_seq);
    }

    return customType;
}

void showMsgSize() {
    MallocMessageBuilder message;
    TestCustomType::Reader reader = initStruct(message, 0).asReader();
    cout << "sample = " << reader.totalSize().wordCount << endl;
    cout << "sample.test_long = " << sizeof(reader.getTestLong()) << endl;
    cout << "sample.test_octet = " << reader.getTestOctet().size() << endl;
    cout << "sample.test_string = " << reader.getTestString().totalSize().wordCount << endl;
    cout << "sample.test_long_seq = " << reader.getTestLongSeq().totalSize().wordCount << endl;
    cout << "sample.test_string_seq = " << reader.getTestStringSeq().totalSize().wordCount << endl;
    cout << "sample.test_double_seq = " << reader.getTestDoubleSeq().totalSize().wordCount << endl;
    cout << "sample.test_array_long_seq = " << reader.getTestArrayLongSeq().totalSize().wordCount << endl;
    cout << "sample.seq_array_long_seq_test = " << reader.getSeqArrayLongSeqTest().totalSize().wordCount << endl;
}

double obtain_serialization_time_cost() {
    MallocMessageBuilder message;
    initStruct(message, 0);
    auto serializedSize = computeSerializedSizeInWords(message);
    double time_cost = 0;
    for (int i = 0; i < NUM_INTER; ++i) {
        TestPipe writer_buf(serializedSize);
        auto start_serial = currentTime();
        writePackedMessage(writer_buf, message);
        auto end_serial = currentTime();
        time_cost += std::chrono::duration_cast<std::chrono::microseconds>(end_serial-start_serial).count();
    }
    return time_cost/NUM_INTER;
}

double obtain_deserialization_time_cost() {
    MallocMessageBuilder message;
    initStruct(message, 0);
    TestPipe buffer;

    double time_cost = 0;
    for (int i = 0; i < NUM_INTER; ++i) {
        writePackedMessage(buffer, message);
        auto start_deserial = currentTime();
        PackedMessageReader reader(buffer);
        auto end_deserial = currentTime();
        time_cost += std::chrono::duration_cast<std::chrono::microseconds>(end_deserial-start_deserial).count();
    }
    return time_cost/NUM_INTER;
}

int main() {
    double avg_serial_time = obtain_serialization_time_cost();
    double avg_deserial_time = obtain_deserialization_time_cost();
    cout << "Serialization / Deserialization : " << avg_serial_time << " / " << avg_deserial_time << " us" << endl;
    showMsgSize();
    return 0;
}