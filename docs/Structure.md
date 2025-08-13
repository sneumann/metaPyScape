# Structure


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 
**representation** | **str** |  | 

## Example

```python
from metaPyScape.models.structure import Structure

# TODO update the JSON string below
json = "{}"
# create an instance of Structure from a JSON string
structure_instance = Structure.from_json(json)
# print the JSON string representation of the object
print(Structure.to_json())

# convert the object into a dict
structure_dict = structure_instance.to_dict()
# create an instance of Structure from a dict
structure_from_dict = Structure.from_dict(structure_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


