# FeatureEims


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**feature_ion** | [**FeatureIon**](FeatureIon.md) |  | [optional] 
**eims** | [**List[Mobilogram]**](Mobilogram.md) |  | [optional] 

## Example

```python
from metaPyScape.models.feature_eims import FeatureEims

# TODO update the JSON string below
json = "{}"
# create an instance of FeatureEims from a JSON string
feature_eims_instance = FeatureEims.from_json(json)
# print the JSON string representation of the object
print(FeatureEims.to_json())

# convert the object into a dict
feature_eims_dict = feature_eims_instance.to_dict()
# create an instance of FeatureEims from a dict
feature_eims_from_dict = FeatureEims.from_dict(feature_eims_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


