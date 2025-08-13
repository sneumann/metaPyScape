# metaPyScape.SamplesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**list_all_samples**](SamplesApi.md#list_all_samples) | **GET** /samples/{featureTableId}/list | List All Samples


# **list_all_samples**
> List[Sample] list_all_samples(feature_table_id)

List All Samples

This operation retrieves a list of all samples for a specific feature table identified by the 'featureTableId' path parameter.

### Example


```python
import metaPyScape
from metaPyScape.models.sample import Sample
from metaPyScape.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = metaPyScape.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with metaPyScape.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = metaPyScape.SamplesApi(api_client)
    feature_table_id = 'feature_table_id_example' # str | The unique identifier of the feature table for which the samples are to be retrieved.

    try:
        # List All Samples
        api_response = api_instance.list_all_samples(feature_table_id)
        print("The response of SamplesApi->list_all_samples:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SamplesApi->list_all_samples: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **feature_table_id** | **str**| The unique identifier of the feature table for which the samples are to be retrieved. | 

### Return type

[**List[Sample]**](Sample.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful operation, the list of all samples is retrieved. |  -  |
**500** | An internal server error occurred. Returns an &#39;ErrorResponse&#39; object with details about the error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

