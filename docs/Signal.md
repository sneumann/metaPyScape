# Signal


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**mz** | **float** | m/z value in Da | [optional] 
**intensity** | **float** | absolute intensity | [optional] 
**width** | **float** | the peak width at the given m/z and intensity (can be 0 for MS/MS spectra) | [optional] 

## Example

```python
from metaPyScape.models.signal import Signal

# TODO update the JSON string below
json = "{}"
# create an instance of Signal from a JSON string
signal_instance = Signal.from_json(json)
# print the JSON string representation of the object
print(Signal.to_json())

# convert the object into a dict
signal_dict = signal_instance.to_dict()
# create an instance of Signal from a dict
signal_from_dict = Signal.from_dict(signal_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


