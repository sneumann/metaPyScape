# MainIonDetails


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**feature_id** | **str** |  | [optional] 
**main_ion_notation** | **str** |  | [optional] 
**mz** | **float** |  | [optional] 
**may_reassign_primary_ion** | **bool** |  | [optional] 
**retention_time_in_seconds** | **float** |  | [optional] 
**ccs** | **float** |  | [optional] 
**ms_spectrum** | [**MsSpectrum**](MsSpectrum.md) |  | [optional] 
**ms_ms_spectrum** | [**MsMsSpectrum**](MsMsSpectrum.md) |  | [optional] 
**ms_ms_spectrum_deiso** | [**MsMsSpectrum**](MsMsSpectrum.md) |  | [optional] 

## Example

```python
from metaPyScape.models.main_ion_details import MainIonDetails

# TODO update the JSON string below
json = "{}"
# create an instance of MainIonDetails from a JSON string
main_ion_details_instance = MainIonDetails.from_json(json)
# print the JSON string representation of the object
print(MainIonDetails.to_json())

# convert the object into a dict
main_ion_details_dict = main_ion_details_instance.to_dict()
# create an instance of MainIonDetails from a dict
main_ion_details_from_dict = MainIonDetails.from_dict(main_ion_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


