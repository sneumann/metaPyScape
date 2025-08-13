# MsSpectrum


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**signals** | [**List[Signal]**](Signal.md) |  | [optional] 
**analysis_id** | **str** |  | [optional] 
**mean_measured_mz** | **float** |  | [optional] 
**rt_in_seconds** | **float** |  | [optional] 
**ccs** | **float** |  | [optional] 

## Example

```python
from metaPyScape.models.ms_spectrum import MsSpectrum

# TODO update the JSON string below
json = "{}"
# create an instance of MsSpectrum from a JSON string
ms_spectrum_instance = MsSpectrum.from_json(json)
# print the JSON string representation of the object
print(MsSpectrum.to_json())

# convert the object into a dict
ms_spectrum_dict = ms_spectrum_instance.to_dict()
# create an instance of MsSpectrum from a dict
ms_spectrum_from_dict = MsSpectrum.from_dict(ms_spectrum_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


