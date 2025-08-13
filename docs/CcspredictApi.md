# metaPyScape.CcspredictApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**list_ccs_predict_models**](CcspredictApi.md#list_ccs_predict_models) | **GET** /ccspredict/models | Returns a list of all available CCS Prediction models
[**predict_ccs**](CcspredictApi.md#predict_ccs) | **POST** /ccspredict/models/{modelId} | Predict CCS value for a given structure

# **list_ccs_predict_models**
> list[ModelMetaInfo] list_ccs_predict_models()

Returns a list of all available CCS Prediction models

### Example
```python
from __future__ import print_function
import time
import metaPyScape
from metaPyScape.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = metaPyScape.CcspredictApi()

try:
    # Returns a list of all available CCS Prediction models
    api_response = api_instance.list_ccs_predict_models()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CcspredictApi->list_ccs_predict_models: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[ModelMetaInfo]**](ModelMetaInfo.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **predict_ccs**
> list[CCSPredictResult] predict_ccs(model_id, body=body)

Predict CCS value for a given structure

This endpoint predicts a CCS (Collision Cross Section) value for a given structure. It uses the CCS-Predict model specified by the 'modelId' path parameter. The model is retrieved from the Model Meta Information, which can be obtained through the '/ccspredict/models' endpoint. Please copy the structure type identifiers from the Model Meta Information.

### Example
```python
from __future__ import print_function
import time
import metaPyScape
from metaPyScape.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = metaPyScape.CcspredictApi()
model_id = 'model_id_example' # str | 
body = metaPyScape.Structure() # Structure |  (optional)

try:
    # Predict CCS value for a given structure
    api_response = api_instance.predict_ccs(model_id, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CcspredictApi->predict_ccs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **model_id** | **str**|  | 
 **body** | [**Structure**](Structure.md)|  | [optional] 

### Return type

[**list[CCSPredictResult]**](CCSPredictResult.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: */*
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

