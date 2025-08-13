# metaPyScape.CcspredictApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**list_ccs_predict_models**](CcspredictApi.md#list_ccs_predict_models) | **GET** /ccspredict/models | Returns a list of all available CCS Prediction models
[**predict_ccs**](CcspredictApi.md#predict_ccs) | **POST** /ccspredict/models/{modelId} | Predict CCS value for a given structure


# **list_ccs_predict_models**
> List[ModelMetaInfo] list_ccs_predict_models()

Returns a list of all available CCS Prediction models

### Example


```python
import metaPyScape
from metaPyScape.models.model_meta_info import ModelMetaInfo
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
    api_instance = metaPyScape.CcspredictApi(api_client)

    try:
        # Returns a list of all available CCS Prediction models
        api_response = api_instance.list_ccs_predict_models()
        print("The response of CcspredictApi->list_ccs_predict_models:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CcspredictApi->list_ccs_predict_models: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[ModelMetaInfo]**](ModelMetaInfo.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request accepted. |  -  |
**500** | An internal server error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **predict_ccs**
> List[CCSPredictResult] predict_ccs(model_id, structure=structure)

Predict CCS value for a given structure

This endpoint predicts a CCS (Collision Cross Section) value for a given structure. It uses the CCS-Predict model specified by the 'modelId' path parameter. The model is retrieved from the Model Meta Information, which can be obtained through the '/ccspredict/models' endpoint. Please copy the structure type identifiers from the Model Meta Information.

### Example


```python
import metaPyScape
from metaPyScape.models.ccs_predict_result import CCSPredictResult
from metaPyScape.models.structure import Structure
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
    api_instance = metaPyScape.CcspredictApi(api_client)
    model_id = 'model_id_example' # str | 
    structure = metaPyScape.Structure() # Structure |  (optional)

    try:
        # Predict CCS value for a given structure
        api_response = api_instance.predict_ccs(model_id, structure=structure)
        print("The response of CcspredictApi->predict_ccs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CcspredictApi->predict_ccs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **model_id** | **str**|  | 
 **structure** | [**Structure**](Structure.md)|  | [optional] 

### Return type

[**List[CCSPredictResult]**](CCSPredictResult.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request accepted |  -  |
**500** | An internal server error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

