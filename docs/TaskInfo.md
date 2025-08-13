# TaskInfo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**task_id** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**status** | **str** |  | [optional] 
**progress_value** | **float** |  | [optional] 

## Example

```python
from metaPyScape.models.task_info import TaskInfo

# TODO update the JSON string below
json = "{}"
# create an instance of TaskInfo from a JSON string
task_info_instance = TaskInfo.from_json(json)
# print the JSON string representation of the object
print(TaskInfo.to_json())

# convert the object into a dict
task_info_dict = task_info_instance.to_dict()
# create an instance of TaskInfo from a dict
task_info_from_dict = TaskInfo.from_dict(task_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


