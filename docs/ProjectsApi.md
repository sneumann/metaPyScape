# metaPyScape.ProjectsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_project**](ProjectsApi.md#create_project) | **POST** /projects/create | Create a new project
[**get_task_status**](ProjectsApi.md#get_task_status) | **GET** /projects/taskstatus | Get Task Status
[**list_all_projects**](ProjectsApi.md#list_all_projects) | **GET** /projects/list | List All Projects
[**retrieve_project**](ProjectsApi.md#retrieve_project) | **GET** /projects/{projectId} | Retrieve Project
[**retrieve_project_info**](ProjectsApi.md#retrieve_project_info) | **GET** /projects/info/{projectId} | Retrieve Project Info


# **create_project**
> ProjectTaskSummary create_project(body)

Create a new project

This operation initiates the creation of a project by processing the provided project YAML. This YAML should define the project's structure, including details about experiments and feature tables.

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
    api_instance = metaPyScape.ProjectsApi(api_client)
    body = 'body_example' # str | The YAML file that defines the structure and details of the project, including one experiment and one Feature Table.

    try:
        # Create a new project
        api_response = api_instance.create_project(body)
        print("The response of ProjectsApi->create_project:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectsApi->create_project: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **str**| The YAML file that defines the structure and details of the project, including one experiment and one Feature Table. | 

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
**202** | Project successfully initiated. The response will include details (names and identifiers) about the created project, associated experiments, feature tables, and the ID of the started task. |  -  |
**500** | Internal server error. This can be due to invalid YAML structure, server misconfiguration, or other unexpected issues. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_task_status**
> WorkflowTaskInfo get_task_status(workflow_task_id)

Get Task Status

This endpoint provides the current status of a project task. Clients are advised to poll this endpoint every minute until the task status reaches 'done', 'canceled' or 'failed'.

### Example


```python
import metaPyScape
from metaPyScape.models.workflow_task_info import WorkflowTaskInfo
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
    api_instance = metaPyScape.ProjectsApi(api_client)
    workflow_task_id = 'workflow_task_id_example' # str | ID of the project task to retrieve its status.

    try:
        # Get Task Status
        api_response = api_instance.get_task_status(workflow_task_id)
        print("The response of ProjectsApi->get_task_status:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectsApi->get_task_status: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workflow_task_id** | **str**| ID of the project task to retrieve its status. | 

### Return type

[**WorkflowTaskInfo**](WorkflowTaskInfo.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** | The task is still in processing. The response includes the name and ID of the ongoing task. |  -  |
**200** | The task has completed, either successfully or with errors. The response includes the name and ID of the completed task. |  -  |
**500** | An internal server error occurred. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_all_projects**
> List[Project] list_all_projects()

List All Projects

This operation retrieves a list of all projects.

### Example


```python
import metaPyScape
from metaPyScape.models.project import Project
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
    api_instance = metaPyScape.ProjectsApi(api_client)

    try:
        # List All Projects
        api_response = api_instance.list_all_projects()
        print("The response of ProjectsApi->list_all_projects:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectsApi->list_all_projects: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[Project]**](Project.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful operation, the list of all projects is retrieved. |  -  |
**500** | An internal server error occurred. Returns an &#39;ErrorResponse&#39; object with details about the error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_project**
> Project retrieve_project(project_id)

Retrieve Project

This operation retrieves a project identified by the 'projectId' path parameter.

### Example


```python
import metaPyScape
from metaPyScape.models.project import Project
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
    api_instance = metaPyScape.ProjectsApi(api_client)
    project_id = 'project_id_example' # str | The unique identifier of the project to be retrieved.

    try:
        # Retrieve Project
        api_response = api_instance.retrieve_project(project_id)
        print("The response of ProjectsApi->retrieve_project:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectsApi->retrieve_project: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| The unique identifier of the project to be retrieved. | 

### Return type

[**Project**](Project.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful operation, the project is retrieved. |  -  |
**500** | An internal server error occurred. Returns an &#39;ErrorResponse&#39; object with details about the error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_project_info**
> ProjectInfo retrieve_project_info(project_id)

Retrieve Project Info

This operation retrieves information about a project identified by the 'projectId' path parameter.

### Example


```python
import metaPyScape
from metaPyScape.models.project_info import ProjectInfo
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
    api_instance = metaPyScape.ProjectsApi(api_client)
    project_id = 'project_id_example' # str | The unique identifier of the project for which the information is to be retrieved.

    try:
        # Retrieve Project Info
        api_response = api_instance.retrieve_project_info(project_id)
        print("The response of ProjectsApi->retrieve_project_info:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectsApi->retrieve_project_info: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| The unique identifier of the project for which the information is to be retrieved. | 

### Return type

[**ProjectInfo**](ProjectInfo.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful operation, the project information is retrieved. |  -  |
**500** | An internal server error occurred. Returns an &#39;ErrorResponse&#39; object with details about the error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

