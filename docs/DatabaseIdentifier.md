# DatabaseIdentifier


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**label** | **str** |  | [optional] 
**identifier** | **str** |  | [optional] 

## Example

```python
from metaPyScape.models.database_identifier import DatabaseIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of DatabaseIdentifier from a JSON string
database_identifier_instance = DatabaseIdentifier.from_json(json)
# print the JSON string representation of the object
print(DatabaseIdentifier.to_json())

# convert the object into a dict
database_identifier_dict = database_identifier_instance.to_dict()
# create an instance of DatabaseIdentifier from a dict
database_identifier_from_dict = DatabaseIdentifier.from_dict(database_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


