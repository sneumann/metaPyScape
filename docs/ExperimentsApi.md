# metaPyScape.ExperimentsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_experiment**](ExperimentsApi.md#create_experiment) | **POST** /experiments/create | Create a new experiment


# **create_experiment**
> ProjectTaskSummary create_experiment(body)

Create a new experiment

This operation initiates the creation of an experiment by processing the provided project YAML. This YAML should define the project id and details about the experiment and feature table to be created.

### Example


```python
import metaPyScape
from metaPyScape.models.project_task_summary import ProjectTaskSummary
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
    api_instance = metaPyScape.ExperimentsApi(api_client)
    body = 'body_example' # str | The YAML file that references a project, and defines the structure of one experiment and one Feature Table. The Project ID is mandatory to create an experiment!

    try:
        # Create a new experiment
        api_response = api_instance.create_experiment(body)
        print("The response of ExperimentsApi->create_experiment:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExperimentsApi->create_experiment: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **str**| The YAML file that references a project, and defines the structure of one experiment and one Feature Table. The Project ID is mandatory to create an experiment! | 

### Return type

[**ProjectTaskSummary**](ProjectTaskSummary.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: text/plain
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** | Data processing task succesfully initiated. The response will include details (names and identifiers) about the created project, associated experiments, feature tables, and the ID of the started task. |  -  |
**500** | Internal server error. This can be due to invalid YAML structure, server misconfiguration, or other unexpected issues. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

