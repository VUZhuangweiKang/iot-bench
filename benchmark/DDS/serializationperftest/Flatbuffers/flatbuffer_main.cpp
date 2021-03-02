//
// Created by zhuangwei on 10/11/19.
//

#include "flatbuffer_main.h"
#include "flatbuffers/flatbuffers.h"
#include "flatbufIDL_generated.h"
#include "../utl.cpp"

using namespace FlatBufTest;
using namespace std;


pair<double, double> initStruct(int32_t key) {
    flatbuffers::FlatBufferBuilder builder;

    vector<int8_t> octet_v(SIZE_OCTET_ARRAY, key);
    char *str = (char *)malloc(SIZE_TEST_STR);
    sprintf(str, "Hello World!");
    vector<int32_t> long_seq_v;
    vector<flatbuffers::Offset<StringTest>> str_seq_v;
    vector<double> double_seq_v;
    vector<flatbuffers::Offset<LongSeqTest>> array_long_seq_v;
    vector<flatbuffers::Offset<ArrayLongSeqTest>> seq_array_long_seq_v;

    auto f_octet_v = builder.CreateVector(octet_v);
    auto f_str = builder.CreateString(str);
    auto str_test = CreateStringTest(builder, f_str);
    for (int i = 0; i < SIZE_TEST_SEQ; ++i) {
        long_seq_v.emplace_back((int32_t)i);
        str_seq_v.push_back(str_test);
        double_seq_v.emplace_back((double)i);
    }

    auto f_long_seq_v = builder.CreateVector(long_seq_v);
    auto long_seq = CreateLongSeqTest(builder, f_long_seq_v);

    auto f_str_seq_v = builder.CreateVector(str_seq_v);
    auto str_seq = CreateStringSeqTest(builder, f_str_seq_v);

    auto f_double_seq_v = builder.CreateVector(double_seq_v);
    auto double_seq = CreateDoubleSeqTest(builder, f_double_seq_v);

    for (int j = 0; j < SIZE_TEST_ARRAY_SEQ; ++j)
        array_long_seq_v.push_back(long_seq);
    auto f_array_long_seq_v = builder.CreateVector(array_long_seq_v);
    auto array_long_seq = CreateArrayLongSeqTest(builder, f_array_long_seq_v);

    for (int k = 0; k < SIZE_TEST_SEQ_ARRAY_SEQ; ++k)
        seq_array_long_seq_v.push_back(array_long_seq);
    auto f_seq_array_long_seq_v = builder.CreateVector(seq_array_long_seq_v);
    auto seq_array_long_seq = CreateSeqArrayLongSeqTest(builder, f_seq_array_long_seq_v);

    auto start_serial = currentTime();
    auto testCustomType = CreateTestCustomType(builder, key, f_octet_v, long_seq, str_test, str_seq, double_seq, array_long_seq, seq_array_long_seq);
    builder.Finish(testCustomType);
    uint8_t *buf = builder.GetBufferPointer();
    auto end_serial = currentTime();

    double serialization_time = std::chrono::duration_cast<std::chrono::nanoseconds>(end_serial-start_serial).count();

    auto start_deserial = currentTime();
    auto test_custom_type = GetTestCustomType(buf);
    auto end_deserial = currentTime();

    double deserialization_time = std::chrono::duration_cast<std::chrono::nanoseconds>(end_deserial-start_deserial).count();

    if(key == 0) {
        cout << "Serialized Message Size: " << builder.GetSize() << endl;
    }

    builder.ReleaseBufferPointer();
    return make_pair(serialization_time, deserialization_time);
}


int main() {
    double serialization_time = 0.0;
    double deserialization_time = 0.0;

    for (int i = 0; i < NUM_INTER; ++i) {
        pair<double, double> result = initStruct(i);
        serialization_time += result.first;
        deserialization_time += result.second;
    }
    cout << "Avg Serialization Time(ns): " << serialization_time/NUM_INTER << endl;
    cout << "Avg Deserialization Time(ns): " << deserialization_time/NUM_INTER << endl;
}