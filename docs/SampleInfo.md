# SampleInfo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sample_id** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**sample_type** | **str** |  | [optional] 
**creation_date** | **int** |  | [optional] 
**attributes** | [**List[SampleAttribute]**](SampleAttribute.md) |  | [optional] 

## Example

```python
from metaPyScape.models.sample_info import SampleInfo

# TODO update the JSON string below
json = "{}"
# create an instance of SampleInfo from a JSON string
sample_info_instance = SampleInfo.from_json(json)
# print the JSON string representation of the object
print(SampleInfo.to_json())

# convert the object into a dict
sample_info_dict = sample_info_instance.to_dict()
# create an instance of SampleInfo from a dict
sample_info_from_dict = SampleInfo.from_dict(sample_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


