//
// Created by zhuangwei on 10/11/19.
//

#include "capnproto_main.h"
#include <capnp/serialize-packed.h>
#include <capnp/message.h>
using namespace capnp;

class TestPipe: public kj::BufferedInputStream, public kj::OutputStream {
public:
    TestPipe()
            : preferredReadSize(kj::maxValue), readPos(0) {}
    explicit TestPipe(size_t preferredReadSize)
            : preferredReadSize(preferredReadSize), readPos(0) {}
    ~TestPipe() {}

    const std::string& getData() { return data; }

    kj::ArrayPtr<const byte> getArray() {
        return kj::arrayPtr(reinterpret_cast<const byte*>(data.data()), data.size());
    }

    void resetRead(size_t preferredReadSize = kj::maxValue) {
        readPos = 0;
        this->preferredReadSize = preferredReadSize;
    }

    bool allRead() {
        return readPos == data.size();
    }

    void clear(size_t preferredReadSize = kj::maxValue) {
        resetRead(preferredReadSize);
        data.clear();
    }

    void write(const void* buffer, size_t size) override {
        data.append(reinterpret_cast<const char*>(buffer), size);
    }

    size_t tryRead(void* buffer, size_t minBytes, size_t maxBytes) override {
        KJ_ASSERT(maxBytes <= data.size() - readPos, "Overran end of stream.");
        size_t amount = kj::min(maxBytes, kj::max(minBytes, preferredReadSize));
        memcpy(buffer, data.data() + readPos, amount);
        readPos += amount;
        return amount;
    }

    void skip(size_t bytes) override {
        KJ_ASSERT(bytes <= data.size() - readPos, "Overran end of stream.");
        readPos += bytes;
    }

    kj::ArrayPtr<const byte> tryGetReadBuffer() override {
        size_t amount = kj::min(data.size() - readPos, preferredReadSize);
        return kj::arrayPtr(reinterpret_cast<const byte*>(data.data() + readPos), amount);
    }

private:
    size_t preferredReadSize;
    std::string data;
    std::string::size_type readPos;
};