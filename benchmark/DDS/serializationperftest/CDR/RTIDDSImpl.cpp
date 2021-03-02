#ifndef RTI_MICRO
template <typename T>
double RTIDDSImpl<T>::obtain_dds_serialize_time_cost(
        unsigned int sampleSize,
        unsigned int iters)
{
    T data;
    double serializeTime = 0;
    double timeInit = 0;
    double timeFinish = 0;
    bool success = true;
    unsigned int sequenceSize = sampleSize - perftest_cpp::OVERHEAD_BYTES;

    unsigned int maxSizeSerializedSample = 0;
    char *serializeBuffer = NULL;

    /* --- Initialize data --- */
#ifdef RTI_CUSTOM_TYPE
    // std::cout << "customType: " << typeid(data.custom_type).name() << std::endl;
    initialize_custom_type_data(data.custom_type);
    set_custom_type_data(data.custom_type, 0, sampleSize);

#else
    data.entity_id = 0;
    data.seq_num = 0;
    data.timestamp_sec = 0;
    data.timestamp_usec = 0;
    data.latency_ping = 0;

    std::cout << "sequenceSize:" << sequenceSize << std::endl;
    data.bin_data.ensure_length(sequenceSize, sequenceSize);

    /* --- Display data types --- */
    std::cout << "data: " << typeid(T).name() << std::endl;
    std::cout << "data.bin_data = " << sizeof(data.bin_data) << std::endl;

#endif

    if (DDS_RETCODE_OK != T::TypeSupport::serialize_data_to_cdr_buffer(
            NULL, maxSizeSerializedSample, &data)) {
        fprintf(stderr,
                "Fail to serialize sample on obtain_dds_serialize_time_cost\n");
        return 0;
    }

    RTIOsapiHeap_allocateBuffer(
            &serializeBuffer,
            maxSizeSerializedSample,
            RTI_OSAPI_ALIGNMENT_DEFAULT);

    /* Serialize time calculating */
    timeInit = (unsigned int) PerftestClock::getInstance().getTimeUsec();

    for (unsigned int i = 0; i < iters; i++) {
#ifdef RTI_CUSTOM_TYPE
        set_custom_type_data(data.custom_type, i, sampleSize);
#endif
        if (DDS_RETCODE_OK != T::TypeSupport::serialize_data_to_cdr_buffer(
                serializeBuffer,
                maxSizeSerializedSample,
                &data)){
            fprintf(stderr,
                    "Fail to serialize sample on obtain_dds_serialize_time_cost\n");
            success = false;
        }
    }

    timeFinish = (unsigned int) PerftestClock::getInstance().getTimeUsec();

    serializeTime = (timeFinish - timeInit) / (float)iters;

    if (serializeBuffer != NULL) {
        RTIOsapiHeap_freeBuffer(serializeBuffer);
    }

    if (!success) {
        return 0;
    }

    return serializeTime;
}

template <typename T>
double RTIDDSImpl<T>::obtain_dds_deserialize_time_cost(
        unsigned int sampleSize,
        unsigned int iters)
{
    T data;
    double timeInit = 0;
    double timeFinish = 0;
    double deSerializeTime = 0;
    bool success = true;
    unsigned int sequenceSize = sampleSize - perftest_cpp::OVERHEAD_BYTES;

    unsigned int maxSizeSerializedSample = 0;
    char *serializeBuffer = NULL;


    /* --- Initialize data --- */
#ifdef RTI_CUSTOM_TYPE
    std::cout << "customType: " << typeid(data.custom_type).name() << std::endl;
    initialize_custom_type_data(data.custom_type);
    set_custom_type_data(data.custom_type, 0, sampleSize);

#else
    unsigned int sequenceSize = sampleSize - perftest_cpp::OVERHEAD_BYTES;
    data.entity_id = 0;
    data.seq_num = 0;
    data.timestamp_sec = 0;
    data.timestamp_usec = 0;
    data.latency_ping = 0;

    std::cout << "sequenceSize:" << sequenceSize << std::endl;
    data.bin_data.ensure_length(sequenceSize, sequenceSize);

    /* --- Display data types --- */
    std::cout << "data: " << typeid(T).name() << std::endl;
    std::cout << "data.bin_data = " << sizeof(data.bin_data) << std::endl;

#endif

    // determine the maxSizeSerializedSample
    if (DDS_RETCODE_OK != T::TypeSupport::serialize_data_to_cdr_buffer(
            NULL,
            maxSizeSerializedSample,
            &data)){
        fprintf(stderr,
                "Fail to serialize sample on obtain_dds_serialize_time_cost\n");
        return 0;
    }

    RTIOsapiHeap_allocateBuffer(
            &serializeBuffer,
            maxSizeSerializedSample,
            RTI_OSAPI_ALIGNMENT_DEFAULT);

    if (serializeBuffer == NULL) {
        fprintf(stderr,
                "Error allocating memory for buffer on "
                "obtain_dds_deserialize_time_cost\n");
        return 0;
    }

    if (DDS_RETCODE_OK != T::TypeSupport::serialize_data_to_cdr_buffer(
            serializeBuffer,
            maxSizeSerializedSample,
            &data)) {
        fprintf(stderr,
                "Fail to serialize sample on obtain_dds_deserialize_time_cost\n");
        return 0;
    }

    /* Deserialize time calculating */
    timeInit = (unsigned int) PerftestClock::getInstance().getTimeUsec();

    for (unsigned int i = 0; i < iters; i++) {
#ifdef RTI_CUSTOM_TYPE
        set_custom_type_data(data.custom_type, i, sampleSize);
#endif
        if (DDS_RETCODE_OK != T::TypeSupport::deserialize_data_from_cdr_buffer(
                &data,
                serializeBuffer,
                maxSizeSerializedSample)) {
            fprintf(stderr,
                    "Fail to deserialize sample on "
                    "obtain_dds_deserialize_time_cost\n");
            success = false;
        }
    }
    timeFinish = (unsigned int) PerftestClock::getInstance().getTimeUsec();
    deSerializeTime = timeFinish - timeInit;

    if (serializeBuffer != NULL) {
        RTIOsapiHeap_freeBuffer(serializeBuffer);
    }

    if (!success) {
        return 0;
    }

    return deSerializeTime / (float) iters;
}
#endif //RTI_MICRO