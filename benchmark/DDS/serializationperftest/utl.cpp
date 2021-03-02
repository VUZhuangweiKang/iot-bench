//
// Created by zhuangwei on 10/8/19.
//

#include <iostream>
#include <numeric>
#include <cmath>
#include <chrono>
using namespace std;
#define NUM_INTER 1000

const long SIZE_TEST_STR = 16;
const long SIZE_TEST_SEQ = 128;
const long SIZE_TEST_ARRAY_SEQ = 4;
const long SIZE_TEST_SEQ_ARRAY_SEQ = 4;
const long SIZE_OCTET_ARRAY = 360;

auto currentTime() {
    auto clock = std::chrono::high_resolution_clock::now();
    return clock;
}