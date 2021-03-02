/*
 * (c) 2005-2018  Copyright, Real-Time Innovations, Inc. All rights reserved.
 * Subject to Eclipse Public License v1.0; see LICENSE.md for details.
 */
#ifdef RTI_CUSTOM_TYPE
#include "CustomType.h"

/*
 * This is the source code file that contains the implementation of the API
 * required to work with the Custom type.
 */

// TODO: Add here the implementation for your custom type


bool initialize_custom_type_data(RTI_CUSTOM_TYPE &data)
{
    // allocate memory for sequences
    bool check_long_seq = data.test_long_seq.test_long_seq.ensure_length(SIZE_TEST_SEQ, SIZE_TEST_SEQ);
    bool check_string_seq = data.test_string_seq.test_string_seq.ensure_length(SIZE_TEST_SEQ, SIZE_TEST_SEQ);
    bool check_double_seq = data.test_double_seq.test_double_seq.ensure_length(SIZE_TEST_SEQ, SIZE_TEST_SEQ);
    bool check_array_long_seq = true;
    
    for (size_t i = 0; i < SIZE_TEST_ARRAY_SEQ; i++)
    {
        check_array_long_seq &= data.test_array_long_seq.test_array_long_seq[i].test_long_seq.ensure_length(SIZE_TEST_SEQ, SIZE_TEST_SEQ);
    }
    bool check_seq_array_long_seq = data.seq_array_long_seq_test.seq_array_long_seq_test.ensure_length(SIZE_TEST_SEQ_ARRAY_SEQ, SIZE_TEST_SEQ_ARRAY_SEQ);

    if (check_long_seq && check_string_seq && check_double_seq && check_array_long_seq && check_seq_array_long_seq)
    {
        return true;
    }
    
    return false;
}

void register_custom_type_data(RTI_CUSTOM_TYPE &data, unsigned long key)
{
    data.test_long = key;
}

bool set_custom_type_data(
        RTI_CUSTOM_TYPE &data,
        unsigned long key,
        int targetDataLen)
{
    data.test_long = key;
    sprintf(data.test_string.test_string, "Hello World!");
    
    for (size_t i = 0; i < SIZE_TEST_SEQ; i++)
    {
        data.test_string_seq.test_string_seq[i] = data.test_string;
        data.test_long_seq.test_long_seq[i] = (long)key;
        data.test_double_seq.test_double_seq[i] = (double)key;
    }
    
    for (size_t i = 0; i < SIZE_TEST_ARRAY_SEQ; i++)
    {
        data.test_array_long_seq.test_array_long_seq[i] = data.test_long_seq;
    }
    
    for (size_t i = 0; i < SIZE_TEST_SEQ_ARRAY_SEQ; i++)
    {
        data.seq_array_long_seq_test.seq_array_long_seq_test[i] = data.test_array_long_seq;
    }
    
    return true;
}

bool finalize_custom_type_data(RTI_CUSTOM_TYPE &data)
{
    return true;
}

bool initialize_custom_type_dynamic_data(DDS_DynamicData &data)
{
    return true;
}

void register_custom_type_dynamic_data(DDS_DynamicData &data, unsigned long key)
{
}

bool set_custom_type_dynamic_data(
        DDS_DynamicData &data,
        unsigned long key,
        int targetDataLen)
{
    return true;
}

bool finalize_custom_type_dynamic_data(DDS_DynamicData &data)
{
    return true;
}

#ifdef RTI_CUSTOM_TYPE_FLATDATA
bool initialize_custom_type_data_flatdata(
        rti::flat::flat_type_traits<RTI_CUSTOM_TYPE_FLATDATA>::builder &data)
{
    return true;
}

void register_custom_type_data_flatdata(
        rti::flat::flat_type_traits<RTI_CUSTOM_TYPE_FLATDATA>::builder &data,
        unsigned long key)
{
}

bool set_custom_type_data_flatdata(
        rti::flat::flat_type_traits<RTI_CUSTOM_TYPE_FLATDATA>::builder &data,
        unsigned long key,
        int targetDataLen)
{
    return true;
}

bool finalize_custom_type_data_flatdata(
        rti::flat::flat_type_traits<RTI_CUSTOM_TYPE_FLATDATA>::builder &data)
{
    return true;
}

#endif // RTI_CUSTOM_TYPE_FLATDATA
#endif // RTI_CUSTOM_TYPE
