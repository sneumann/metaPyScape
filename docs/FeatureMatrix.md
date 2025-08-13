# FeatureMatrix


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**intensities** | **List[List[float]]** |  | [optional] 
**feature_ids** | **List[str]** |  | [optional] 
**analysis_ids** | **List[str]** |  | [optional] 

## Example

```python
from metaPyScape.models.feature_matrix import FeatureMatrix

# TODO update the JSON string below
json = "{}"
# create an instance of FeatureMatrix from a JSON string
feature_matrix_instance = FeatureMatrix.from_json(json)
# print the JSON string representation of the object
print(FeatureMatrix.to_json())

# convert the object into a dict
feature_matrix_dict = feature_matrix_instance.to_dict()
# create an instance of FeatureMatrix from a dict
feature_matrix_from_dict = FeatureMatrix.from_dict(feature_matrix_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


