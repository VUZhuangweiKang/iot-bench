cmake_minimum_required(VERSION 3.5)
project(Serialization CXX)

set(CMAKE_CXX_STANDARD 14)

# Protobuf
find_package(Protobuf REQUIRED)
include_directories(${PROTOBUF_INCLUDE_DIRS})
include_directories(${CMAKE_CURRENT_BINARY_DIR})
protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS Protobuf/ProtobufCustomType.proto)

# Cap'n proto
find_package(CapnProto CONFIG REQUIRED)
capnp_generate_cpp(TestCustomTypeSources TestCustomTypeHeaders CapnProto/TestCustomType.capnp)

# executables
add_executable(msgpack MessagePack/msgpack_main.cpp)
add_executable(protobuf Protobuf/protobuf_main.cpp Protobuf/ProtobufCustomType.proto ${PROTO_SRCS} ${PROTO_HDRS})
add_executable(capnproto CapnProto/capnproto_main.cpp ${TestCustomTypeSources})
add_executable(flatbuf Flatbuffers/flatbuffer_main.cpp)

# link libraries
target_link_libraries(protobuf ${PROTOBUF_LIBRARY})
target_link_libraries(capnproto PRIVATE CapnProto::capnp)
target_include_directories(capnproto PRIVATE ${CMAKE_CURRENT_BINARY_DIR})

# Flatbuffers
set(FLATBUFFERS_CMAKE_DIR ${CMAKE_CURRENT_LIST_DIR})

find_program(FLATBUFFERS_FLATC_EXECUTABLE NAMES flatc)
find_path(FLATBUFFERS_INCLUDE_DIR NAMES flatbuffers/flatbuffers.h)

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(flatbuffers
        DEFAULT_MSG FLATBUFFERS_FLATC_EXECUTABLE FLATBUFFERS_INCLUDE_DIR)