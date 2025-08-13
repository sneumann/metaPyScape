# metaPyScape.SamplesApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**list_all_samples**](SamplesApi.md#list_all_samples) | **GET** /samples/{featureTableId}/list | List All Samples

# **list_all_samples**
> list[Sample] list_all_samples(feature_table_id)

List All Samples

This operation retrieves a list of all samples for a specific feature table identified by the 'featureTableId' path parameter.

### Example
```python
from __future__ import print_function
import time
import metaPyScape
from metaPyScape.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = metaPyScape.SamplesApi()
feature_table_id = 'feature_table_id_example' # str | The unique identifier of the feature table for which the samples are to be retrieved.

try:
    # List All Samples
    api_response = api_instance.list_all_samples(feature_table_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SamplesApi->list_all_samples: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **feature_table_id** | **str**| The unique identifier of the feature table for which the samples are to be retrieved. | 

### Return type

[**list[Sample]**](Sample.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

