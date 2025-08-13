# SampleVolume


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**volume** | **float** |  | [optional] 
**unit** | **str** |  | [optional] 

## Example

```python
from metaPyScape.models.sample_volume import SampleVolume

# TODO update the JSON string below
json = "{}"
# create an instance of SampleVolume from a JSON string
sample_volume_instance = SampleVolume.from_json(json)
# print the JSON string representation of the object
print(SampleVolume.to_json())

# convert the object into a dict
sample_volume_dict = sample_volume_instance.to_dict()
# create an instance of SampleVolume from a dict
sample_volume_from_dict = SampleVolume.from_dict(sample_volume_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


