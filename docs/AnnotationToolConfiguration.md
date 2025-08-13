# AnnotationToolConfiguration


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**scoring_configuration** | [**ScoringConfiguration**](ScoringConfiguration.md) |  | [optional] 

## Example

```python
from metaPyScape.models.annotation_tool_configuration import AnnotationToolConfiguration

# TODO update the JSON string below
json = "{}"
# create an instance of AnnotationToolConfiguration from a JSON string
annotation_tool_configuration_instance = AnnotationToolConfiguration.from_json(json)
# print the JSON string representation of the object
print(AnnotationToolConfiguration.to_json())

# convert the object into a dict
annotation_tool_configuration_dict = annotation_tool_configuration_instance.to_dict()
# create an instance of AnnotationToolConfiguration from a dict
annotation_tool_configuration_from_dict = AnnotationToolConfiguration.from_dict(annotation_tool_configuration_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


