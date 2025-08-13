# AnnotationMethod


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**version** | **str** |  | [optional] 
**active** | **bool** |  | [optional] 
**id** | **str** |  | [optional] 

## Example

```python
from metaPyScape.models.annotation_method import AnnotationMethod

# TODO update the JSON string below
json = "{}"
# create an instance of AnnotationMethod from a JSON string
annotation_method_instance = AnnotationMethod.from_json(json)
# print the JSON string representation of the object
print(AnnotationMethod.to_json())

# convert the object into a dict
annotation_method_dict = annotation_method_instance.to_dict()
# create an instance of AnnotationMethod from a dict
annotation_method_from_dict = AnnotationMethod.from_dict(annotation_method_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


