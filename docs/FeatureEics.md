# FeatureEics


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**feature_ion** | [**FeatureIon**](FeatureIon.md) |  | [optional] 
**eics** | [**List[Chromatogram]**](Chromatogram.md) |  | [optional] 

## Example

```python
from metaPyScape.models.feature_eics import FeatureEics

# TODO update the JSON string below
json = "{}"
# create an instance of FeatureEics from a JSON string
feature_eics_instance = FeatureEics.from_json(json)
# print the JSON string representation of the object
print(FeatureEics.to_json())

# convert the object into a dict
feature_eics_dict = feature_eics_instance.to_dict()
# create an instance of FeatureEics from a dict
feature_eics_from_dict = FeatureEics.from_dict(feature_eics_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


