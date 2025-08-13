# ModelMetaInfo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**version_number** | **str** |  | [optional] 
**available_ion_notations** | **List[str]** |  | [optional] 
**available_structure_types** | **List[str]** |  | [optional] 

## Example

```python
from metaPyScape.models.model_meta_info import ModelMetaInfo

# TODO update the JSON string below
json = "{}"
# create an instance of ModelMetaInfo from a JSON string
model_meta_info_instance = ModelMetaInfo.from_json(json)
# print the JSON string representation of the object
print(ModelMetaInfo.to_json())

# convert the object into a dict
model_meta_info_dict = model_meta_info_instance.to_dict()
# create an instance of ModelMetaInfo from a dict
model_meta_info_from_dict = ModelMetaInfo.from_dict(model_meta_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


