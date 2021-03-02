#include <msgpack.hpp>
#include "MsgPackCustomType.h"

using namespace msgpack;

TestCustomType initStruct(int32_t msgID) {
    TestCustomType customType;
    customType.test_long = (long)msgID;
    for (int i = 0; i < SIZE_OCTET_ARRAY; ++i) {
        customType.test_octet[i] = (octet) i;
    }

    sprintf(customType.test_string.str, "Hello world!");

    for (int j = 0; j < SIZE_TEST_SEQ; ++j) {
        customType.test_long_seq.long_seq[j] = customType.test_long;
        customType.test_string_seq.string_seq[j] = customType.test_string;
        customType.test_double_seq.double_seq[j] = (double)j;
    }

    for (auto & k : customType.test_array_long_seq.array_long_seq) {
        k = customType.test_long_seq;
    }

    for (auto & l : customType.seq_array_long_seq_test.seq_array_long_seq) {
        l = customType.test_array_long_seq;
    }

    return customType;
}

void showMsgSize() {
    TestCustomType sample = initStruct(1);
    cout << "sample = " << sizeof(sample) << endl;
    cout << "sample.test_long = " << sizeof(sample.test_long) << endl;
    cout << "sample.test_octet = " << sizeof(sample.test_octet) << endl;
    cout << "sample.test_string = " << sizeof(sample.test_string) << endl;
    cout << "sample.test_long_seq = " << sizeof(sample.test_long_seq) << endl;
    cout << "sample.test_string_seq = " << sizeof(sample.test_string_seq) << endl;
    cout << "sample.test_double_seq = " << sizeof(sample.test_double_seq) << endl;
    cout << "sample.test_array_long_seq = " << sizeof(sample.test_array_long_seq) << endl;
    cout << "sample.seq_array_long_seq_test = " << sizeof(sample.seq_array_long_seq_test) << endl;
}

double obtain_serialization_time_cost() {
    /* determine required buffer size */
    TestCustomType testData = initStruct(1);
    sbuffer temp;
    pack(temp, testData);
    unsigned long bufferSize = temp.size();
    temp.release();

    sbuffer sbuf(bufferSize); // allocate buffer
    auto start_serial = currentTime();
    for (size_t i = 0; i < NUM_INTER; i++)
    {
        pack(sbuf, testData);
    }
    auto end_serial = currentTime();
    sbuf.release(); // release buffer
    return std::chrono::duration_cast<std::chrono::microseconds>(end_serial-start_serial).count()/NUM_INTER;
}

double obtain_deserialization_time_cost() {
    sbuffer sbuf;
    TestCustomType testData = initStruct(1);
    pack(sbuf, testData);
    unpacked msg; // deserialize message
    auto start_deserial = currentTime();
    for (size_t i = 0; i < NUM_INTER; i++)
    {
        unpack(&msg, sbuf.data(), sbuf.size());
    }
    auto end_deserial = currentTime();
    sbuf.release(); // release buffer
    return std::chrono::duration_cast<std::chrono::microseconds>(end_deserial-start_deserial).count()/NUM_INTER;
}

int main() {
    double avg_serial_time = obtain_serialization_time_cost();
    double avg_deserial_time = obtain_deserialization_time_cost();
    cout << "Serialization / Deserialization : " << avg_serial_time << " / " << avg_deserial_time << " us" << endl;
    showMsgSize();
    return 0;
}
