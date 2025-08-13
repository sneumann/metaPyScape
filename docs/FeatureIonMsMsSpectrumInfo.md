# FeatureIonMsMsSpectrumInfo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**feature_id** | **str** |  | [optional] 
**feature_ion** | [**FeatureIon**](FeatureIon.md) |  | [optional] 
**spectra** | [**List[MsMsSpectrum]**](MsMsSpectrum.md) |  | [optional] 

## Example

```python
from metaPyScape.models.feature_ion_ms_ms_spectrum_info import FeatureIonMsMsSpectrumInfo

# TODO update the JSON string below
json = "{}"
# create an instance of FeatureIonMsMsSpectrumInfo from a JSON string
feature_ion_ms_ms_spectrum_info_instance = FeatureIonMsMsSpectrumInfo.from_json(json)
# print the JSON string representation of the object
print(FeatureIonMsMsSpectrumInfo.to_json())

# convert the object into a dict
feature_ion_ms_ms_spectrum_info_dict = feature_ion_ms_ms_spectrum_info_instance.to_dict()
# create an instance of FeatureIonMsMsSpectrumInfo from a dict
feature_ion_ms_ms_spectrum_info_from_dict = FeatureIonMsMsSpectrumInfo.from_dict(feature_ion_ms_ms_spectrum_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


