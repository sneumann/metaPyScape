# ProjectTaskSummary


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project** | [**Project**](Project.md) |  | [optional] 
**workflow_task_id** | **str** |  | [optional] 
**task_id** | **str** |  | [optional] 

## Example

```python
from metaPyScape.models.project_task_summary import ProjectTaskSummary

# TODO update the JSON string below
json = "{}"
# create an instance of ProjectTaskSummary from a JSON string
project_task_summary_instance = ProjectTaskSummary.from_json(json)
# print the JSON string representation of the object
print(ProjectTaskSummary.to_json())

# convert the object into a dict
project_task_summary_dict = project_task_summary_instance.to_dict()
# create an instance of ProjectTaskSummary from a dict
project_task_summary_from_dict = ProjectTaskSummary.from_dict(project_task_summary_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


