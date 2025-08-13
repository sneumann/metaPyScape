# SampleAttribute


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**value** | **str** |  | [optional] 

## Example

```python
from metaPyScape.models.sample_attribute import SampleAttribute

# TODO update the JSON string below
json = "{}"
# create an instance of SampleAttribute from a JSON string
sample_attribute_instance = SampleAttribute.from_json(json)
# print the JSON string representation of the object
print(SampleAttribute.to_json())

# convert the object into a dict
sample_attribute_dict = sample_attribute_instance.to_dict()
# create an instance of SampleAttribute from a dict
sample_attribute_from_dict = SampleAttribute.from_dict(sample_attribute_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


