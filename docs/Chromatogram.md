# Chromatogram


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**rts_in_seconds** | **List[float]** |  | [optional] 
**intensities** | **List[float]** |  | [optional] 
**analysis_id** | **str** |  | [optional] 

## Example

```python
from metaPyScape.models.chromatogram import Chromatogram

# TODO update the JSON string below
json = "{}"
# create an instance of Chromatogram from a JSON string
chromatogram_instance = Chromatogram.from_json(json)
# print the JSON string representation of the object
print(Chromatogram.to_json())

# convert the object into a dict
chromatogram_dict = chromatogram_instance.to_dict()
# create an instance of Chromatogram from a dict
chromatogram_from_dict = Chromatogram.from_dict(chromatogram_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


