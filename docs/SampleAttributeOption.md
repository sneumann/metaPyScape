# SampleAttributeOption


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**color** | [**Color**](Color.md) |  | [optional] 
**symbol** | **str** |  | [optional] 

## Example

```python
from metaPyScape.models.sample_attribute_option import SampleAttributeOption

# TODO update the JSON string below
json = "{}"
# create an instance of SampleAttributeOption from a JSON string
sample_attribute_option_instance = SampleAttributeOption.from_json(json)
# print the JSON string representation of the object
print(SampleAttributeOption.to_json())

# convert the object into a dict
sample_attribute_option_dict = sample_attribute_option_instance.to_dict()
# create an instance of SampleAttributeOption from a dict
sample_attribute_option_from_dict = SampleAttributeOption.from_dict(sample_attribute_option_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


