# ExperimentInfo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**experiment_id** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**group_colors** | **str** |  | [optional] 
**group_symbols** | **str** |  | [optional] 
**creation_date** | **int** |  | [optional] 
**samples** | [**List[SampleInfo]**](SampleInfo.md) |  | [optional] 

## Example

```python
from metaPyScape.models.experiment_info import ExperimentInfo

# TODO update the JSON string below
json = "{}"
# create an instance of ExperimentInfo from a JSON string
experiment_info_instance = ExperimentInfo.from_json(json)
# print the JSON string representation of the object
print(ExperimentInfo.to_json())

# convert the object into a dict
experiment_info_dict = experiment_info_instance.to_dict()
# create an instance of ExperimentInfo from a dict
experiment_info_from_dict = ExperimentInfo.from_dict(experiment_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


