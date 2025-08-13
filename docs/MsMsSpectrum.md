# MsMsSpectrum


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**signals** | [**List[Signal]**](Signal.md) |  | [optional] 

## Example

```python
from metaPyScape.models.ms_ms_spectrum import MsMsSpectrum

# TODO update the JSON string below
json = "{}"
# create an instance of MsMsSpectrum from a JSON string
ms_ms_spectrum_instance = MsMsSpectrum.from_json(json)
# print the JSON string representation of the object
print(MsMsSpectrum.to_json())

# convert the object into a dict
ms_ms_spectrum_dict = ms_ms_spectrum_instance.to_dict()
# create an instance of MsMsSpectrum from a dict
ms_ms_spectrum_from_dict = MsMsSpectrum.from_dict(ms_ms_spectrum_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


