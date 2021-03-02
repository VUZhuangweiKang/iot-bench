#!/bin/bash

# install message pack
git clone https://github.com/msgpack/msgpack-c.git
cd msgpack-c
cmake .
make
sudo make install

# install protobuf
sudo apt-get install autoconf automake libtool curl make g++ unzip -y
git clone https://github.com/google/protobuf.git
cd protobuf
git submodule update --init --recursive
./autogen.sh && ./configure
make
make check
sudo make install
sudo ldconfig

# install cap'n proto
curl -O https://capnproto.org/capnproto-c++-0.7.0.tar.gz
tar zxf capnproto-c++-0.7.0.tar.gz
cd capnproto-c++-0.7.0
./configure
make -j6 check
sudo make install

# install flatbuffers
git clone https://github.com/google/flatbuffers.git
cd flatbuffers
cmake -G "Unix Makefiles"
make
make install

