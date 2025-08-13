# AQScores


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**mz_aq_score** | **int** |  | [optional] 
**rt_aq_score** | **int** |  | [optional] 
**isotope_pattern_aq_score** | **int** |  | [optional] 
**msms_aq_score** | **int** |  | [optional] 
**ccs_aq_score** | **int** |  | [optional] 
**mz_deviation** | **float** |  | [optional] 
**rt_deviation** | **float** |  | [optional] 
**isotope_pattern_score** | **float** |  | [optional] 
**msms_score** | **float** |  | [optional] 
**ccs_deviation** | **float** |  | [optional] 
**annotation_modifiers** | **List[Optional[str]]** |  | [optional] 

## Example

```python
from metaPyScape.models.aq_scores import AQScores

# TODO update the JSON string below
json = "{}"
# create an instance of AQScores from a JSON string
aq_scores_instance = AQScores.from_json(json)
# print the JSON string representation of the object
print(AQScores.to_json())

# convert the object into a dict
aq_scores_dict = aq_scores_instance.to_dict()
# create an instance of AQScores from a dict
aq_scores_from_dict = AQScores.from_dict(aq_scores_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


