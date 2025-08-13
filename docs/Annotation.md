# Annotation


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**formula** | **str** |  | [optional] 
**aq_scores** | [**AQScores**](AQScores.md) |  | [optional] 
**tool** | **str** |  | [optional] 
**structure_inchi** | **str** |  | [optional] 
**structure_smiles** | **str** |  | [optional] 
**database_identifiers** | [**List[DatabaseIdentifier]**](DatabaseIdentifier.md) |  | [optional] 
**annotated_ms_ms_fragment_details** | [**List[AnnotatedMsMsFragmentDetails]**](AnnotatedMsMsFragmentDetails.md) |  | [optional] 

## Example

```python
from metaPyScape.models.annotation import Annotation

# TODO update the JSON string below
json = "{}"
# create an instance of Annotation from a JSON string
annotation_instance = Annotation.from_json(json)
# print the JSON string representation of the object
print(Annotation.to_json())

# convert the object into a dict
annotation_dict = annotation_instance.to_dict()
# create an instance of Annotation from a dict
annotation_from_dict = Annotation.from_dict(annotation_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


