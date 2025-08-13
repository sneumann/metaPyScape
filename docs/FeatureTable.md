# FeatureTable


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**polarity** | **str** |  | [optional] 
**processing_workflow** | **str** |  | [optional] 

## Example

```python
from metaPyScape.models.feature_table import FeatureTable

# TODO update the JSON string below
json = "{}"
# create an instance of FeatureTable from a JSON string
feature_table_instance = FeatureTable.from_json(json)
# print the JSON string representation of the object
print(FeatureTable.to_json())

# convert the object into a dict
feature_table_dict = feature_table_instance.to_dict()
# create an instance of FeatureTable from a dict
feature_table_from_dict = FeatureTable.from_dict(feature_table_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


