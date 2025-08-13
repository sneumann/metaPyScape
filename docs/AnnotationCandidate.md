# AnnotationCandidate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**annotation_configuration_id** | **str** |  | 
**molecular_formula** | **str** |  | 
**structure** | [**Structure**](Structure.md) |  | [optional] 
**rt_dev_in_seconds** | **float** |  | [optional] 
**ms_ms_score** | **float** |  | [optional] 
**ccs_dev_in_perc** | **float** |  | [optional] 

## Example

```python
from metaPyScape.models.annotation_candidate import AnnotationCandidate

# TODO update the JSON string below
json = "{}"
# create an instance of AnnotationCandidate from a JSON string
annotation_candidate_instance = AnnotationCandidate.from_json(json)
# print the JSON string representation of the object
print(AnnotationCandidate.to_json())

# convert the object into a dict
annotation_candidate_dict = annotation_candidate_instance.to_dict()
# create an instance of AnnotationCandidate from a dict
annotation_candidate_from_dict = AnnotationCandidate.from_dict(annotation_candidate_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


