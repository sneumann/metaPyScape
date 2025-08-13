# Color


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**hex** | **str** |  | [optional] 
**name** | **str** |  | [optional] 

## Example

```python
from metaPyScape.models.color import Color

# TODO update the JSON string below
json = "{}"
# create an instance of Color from a JSON string
color_instance = Color.from_json(json)
# print the JSON string representation of the object
print(Color.to_json())

# convert the object into a dict
color_dict = color_instance.to_dict()
# create an instance of Color from a dict
color_from_dict = Color.from_dict(color_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


