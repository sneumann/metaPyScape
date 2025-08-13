# CCSPredictResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**structure** | [**Structure**](Structure.md) |  | [optional] 
**ion_notation** | **str** |  | [optional] 
**predicted_ccs** | **float** |  | [optional] 
**result_message** | **str** |  | [optional] 

## Example

```python
from metaPyScape.models.ccs_predict_result import CCSPredictResult

# TODO update the JSON string below
json = "{}"
# create an instance of CCSPredictResult from a JSON string
ccs_predict_result_instance = CCSPredictResult.from_json(json)
# print the JSON string representation of the object
print(CCSPredictResult.to_json())

# convert the object into a dict
ccs_predict_result_dict = ccs_predict_result_instance.to_dict()
# create an instance of CCSPredictResult from a dict
ccs_predict_result_from_dict = CCSPredictResult.from_dict(ccs_predict_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


