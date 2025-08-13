# ScoringConfiguration


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**mz_wide** | **float** |  | 
**mz_narrow** | **float** |  | 
**mz_unit** | **str** |  | 
**rt_in_seconds_narrow** | **float** |  | [optional] 
**rt_in_seconds_wide** | **float** |  | [optional] 
**ms_ms_wide** | **float** |  | [optional] 
**ms_ms_narrow** | **float** |  | [optional] 
**ccs_wide** | **float** |  | [optional] 
**ccs_narrow** | **float** |  | [optional] 
**msigma_narrow** | **float** |  | [optional] 
**msigma_wide** | **float** |  | [optional] 

## Example

```python
from metaPyScape.models.scoring_configuration import ScoringConfiguration

# TODO update the JSON string below
json = "{}"
# create an instance of ScoringConfiguration from a JSON string
scoring_configuration_instance = ScoringConfiguration.from_json(json)
# print the JSON string representation of the object
print(ScoringConfiguration.to_json())

# convert the object into a dict
scoring_configuration_dict = scoring_configuration_instance.to_dict()
# create an instance of ScoringConfiguration from a dict
scoring_configuration_from_dict = ScoringConfiguration.from_dict(scoring_configuration_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


