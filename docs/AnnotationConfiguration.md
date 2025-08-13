# AnnotationConfiguration


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ions_for_reassignment** | **List[str]** |  | [optional] 
**main_ion_infos** | [**List[MainIonDetails]**](MainIonDetails.md) |  | [optional] 

## Example

```python
from metaPyScape.models.annotation_configuration import AnnotationConfiguration

# TODO update the JSON string below
json = "{}"
# create an instance of AnnotationConfiguration from a JSON string
annotation_configuration_instance = AnnotationConfiguration.from_json(json)
# print the JSON string representation of the object
print(AnnotationConfiguration.to_json())

# convert the object into a dict
annotation_configuration_dict = annotation_configuration_instance.to_dict()
# create an instance of AnnotationConfiguration from a dict
annotation_configuration_from_dict = AnnotationConfiguration.from_dict(annotation_configuration_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


