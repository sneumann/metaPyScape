# SampleAttributeType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**detailed_attribute_options** | [**List[SampleAttributeOption]**](SampleAttributeOption.md) |  | [optional] 

## Example

```python
from metaPyScape.models.sample_attribute_type import SampleAttributeType

# TODO update the JSON string below
json = "{}"
# create an instance of SampleAttributeType from a JSON string
sample_attribute_type_instance = SampleAttributeType.from_json(json)
# print the JSON string representation of the object
print(SampleAttributeType.to_json())

# convert the object into a dict
sample_attribute_type_dict = sample_attribute_type_instance.to_dict()
# create an instance of SampleAttributeType from a dict
sample_attribute_type_from_dict = SampleAttributeType.from_dict(sample_attribute_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


