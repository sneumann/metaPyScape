# FeatureIon


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ion_notation** | **str** |  | [optional] 
**mz** | **float** |  | [optional] 
**ccs** | **float** |  | [optional] 
**id** | **str** |  | [optional] 
**main_ion** | **bool** |  | [optional] 

## Example

```python
from metaPyScape.models.feature_ion import FeatureIon

# TODO update the JSON string below
json = "{}"
# create an instance of FeatureIon from a JSON string
feature_ion_instance = FeatureIon.from_json(json)
# print the JSON string representation of the object
print(FeatureIon.to_json())

# convert the object into a dict
feature_ion_dict = feature_ion_instance.to_dict()
# create an instance of FeatureIon from a dict
feature_ion_from_dict = FeatureIon.from_dict(feature_ion_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


