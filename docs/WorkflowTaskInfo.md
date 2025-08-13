# WorkflowTaskInfo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**workflow_task_id** | **str** |  | [optional] 
**status** | **str** |  | [optional] 
**task_infos** | [**List[TaskInfo]**](TaskInfo.md) |  | [optional] 

## Example

```python
from metaPyScape.models.workflow_task_info import WorkflowTaskInfo

# TODO update the JSON string below
json = "{}"
# create an instance of WorkflowTaskInfo from a JSON string
workflow_task_info_instance = WorkflowTaskInfo.from_json(json)
# print the JSON string representation of the object
print(WorkflowTaskInfo.to_json())

# convert the object into a dict
workflow_task_info_dict = workflow_task_info_instance.to_dict()
# create an instance of WorkflowTaskInfo from a dict
workflow_task_info_from_dict = WorkflowTaskInfo.from_dict(workflow_task_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


