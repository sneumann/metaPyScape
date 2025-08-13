# Mobilogram


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**inverse_ion_mobilities** | **List[float]** |  | [optional] 
**intensities** | **List[float]** |  | [optional] 
**analysis_id** | **str** |  | [optional] 

## Example

```python
from metaPyScape.models.mobilogram import Mobilogram

# TODO update the JSON string below
json = "{}"
# create an instance of Mobilogram from a JSON string
mobilogram_instance = Mobilogram.from_json(json)
# print the JSON string representation of the object
print(Mobilogram.to_json())

# convert the object into a dict
mobilogram_dict = mobilogram_instance.to_dict()
# create an instance of Mobilogram from a dict
mobilogram_from_dict = Mobilogram.from_dict(mobilogram_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


