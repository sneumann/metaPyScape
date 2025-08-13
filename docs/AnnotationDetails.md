# AnnotationDetails


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**annotation** | [**Annotation**](Annotation.md) |  | [optional] 
**main_ion_notation** | **str** |  | [optional] 

## Example

```python
from metaPyScape.models.annotation_details import AnnotationDetails

# TODO update the JSON string below
json = "{}"
# create an instance of AnnotationDetails from a JSON string
annotation_details_instance = AnnotationDetails.from_json(json)
# print the JSON string representation of the object
print(AnnotationDetails.to_json())

# convert the object into a dict
annotation_details_dict = annotation_details_instance.to_dict()
# create an instance of AnnotationDetails from a dict
annotation_details_from_dict = AnnotationDetails.from_dict(annotation_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


