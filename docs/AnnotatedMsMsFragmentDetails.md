# AnnotatedMsMsFragmentDetails


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fragment_ion_formula** | **str** |  | [optional] 
**accurate_mz** | **float** |  | [optional] 
**ms_ms_spectrum_id** | **str** |  | [optional] 
**ms_ms_rule_type** | **str** |  | [optional] 
**lipid_identity_level** | **str** |  | [optional] 
**chain_information** | **str** |  | [optional] 

## Example

```python
from metaPyScape.models.annotated_ms_ms_fragment_details import AnnotatedMsMsFragmentDetails

# TODO update the JSON string below
json = "{}"
# create an instance of AnnotatedMsMsFragmentDetails from a JSON string
annotated_ms_ms_fragment_details_instance = AnnotatedMsMsFragmentDetails.from_json(json)
# print the JSON string representation of the object
print(AnnotatedMsMsFragmentDetails.to_json())

# convert the object into a dict
annotated_ms_ms_fragment_details_dict = annotated_ms_ms_fragment_details_instance.to_dict()
# create an instance of AnnotatedMsMsFragmentDetails from a dict
annotated_ms_ms_fragment_details_from_dict = AnnotatedMsMsFragmentDetails.from_dict(annotated_ms_ms_fragment_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


