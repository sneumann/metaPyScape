# metaPyScape.ExperimentsApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_experiment**](ExperimentsApi.md#create_experiment) | **POST** /experiments/create | Create a new experiment

# **create_experiment**
> ProjectTaskSummary create_experiment(body)

Create a new experiment

This operation initiates the creation of an experiment by processing the provided project YAML. This YAML should define the project id and details about the experiment and feature table to be created.

### Example
```python
from __future__ import print_function
import time
import metaPyScape
from metaPyScape.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = metaPyScape.ExperimentsApi()
body = 'body_example' # str | The YAML file that references a project, and defines the structure of one experiment and one Feature Table. The Project ID is mandatory to create an experiment!

try:
    # Create a new experiment
    api_response = api_instance.create_experiment(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExperimentsApi->create_experiment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**str**](str.md)| The YAML file that references a project, and defines the structure of one experiment and one Feature Table. The Project ID is mandatory to create an experiment! | 

### Return type

[**ProjectTaskSummary**](ProjectTaskSummary.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: text/plain
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

