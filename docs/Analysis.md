# Analysis


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**include** | **bool** |  | [optional] 

## Example

```python
from metaPyScape.models.analysis import Analysis

# TODO update the JSON string below
json = "{}"
# create an instance of Analysis from a JSON string
analysis_instance = Analysis.from_json(json)
# print the JSON string representation of the object
print(Analysis.to_json())

# convert the object into a dict
analysis_dict = analysis_instance.to_dict()
# create an instance of Analysis from a dict
analysis_from_dict = Analysis.from_dict(analysis_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


