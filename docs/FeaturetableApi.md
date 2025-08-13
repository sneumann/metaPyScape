# metaPyScape.FeaturetableApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_flag_to_feature**](FeaturetableApi.md#add_flag_to_feature) | **POST** /featuretable/feature/{featureId}/flag/create | Add Flag to Feature
[**create_annotation**](FeaturetableApi.md#create_annotation) | **POST** /featuretable/feature/{featureId}/annotation/create | Create a custom annotation for a specific feature
[**create_feature_table**](FeaturetableApi.md#create_feature_table) | **POST** /featuretable/create | Create a new Feature Table based on a project file
[**create_lipid_species_annotations_with_method**](FeaturetableApi.md#create_lipid_species_annotations_with_method) | **POST** /featuretable/annotation/create/lipidspecies/{annotationMethodUuid} | Create Lipid Species Annotations with Method
[**create_smart_formula_annotations_with_method**](FeaturetableApi.md#create_smart_formula_annotations_with_method) | **POST** /featuretable/annotation/create/smartformula/{annotationMethodUuid} | Create SmartFormula Annotations with Method
[**create_target_list_annotations_with_method**](FeaturetableApi.md#create_target_list_annotations_with_method) | **POST** /featuretable/annotation/create/targetlist/{annotationMethodUuid} | Create Target List Annotations with Method
[**delete_annotation**](FeaturetableApi.md#delete_annotation) | **POST** /featuretable/feature/{featureId}/annotation/delete/{annotationId} | Delete a specific annotation for a specific feature
[**generate_new_eics_and_eims**](FeaturetableApi.md#generate_new_eics_and_eims) | **POST** /featuretable/{featureTableId}/eicsandeims/create | Generate new EICs and EIMs for a specific Feature Table
[**remove_flag_from_feature**](FeaturetableApi.md#remove_flag_from_feature) | **POST** /featuretable/feature/{featureId}/flag/remove | Remove Flag from Feature
[**retrieve_annotation_configuration_by_id**](FeaturetableApi.md#retrieve_annotation_configuration_by_id) | **GET** /featuretable/annotation/configuration/{configurationId} | Retrieve Annotation Configuration by ID
[**retrieve_annotation_methods_by_tool_id**](FeaturetableApi.md#retrieve_annotation_methods_by_tool_id) | **GET** /featuretable/annotation/methods/{toolId} | Retrieve Annotation Methods by Tool ID
[**retrieve_eics_for_feature**](FeaturetableApi.md#retrieve_eics_for_feature) | **GET** /featuretable/feature/{featureId}/eics | Retrieve EICs for a specific feature
[**retrieve_eims_for_feature**](FeaturetableApi.md#retrieve_eims_for_feature) | **GET** /featuretable/feature/{featureId}/eims | Retrieve EIMs for a specific feature
[**retrieve_feature**](FeaturetableApi.md#retrieve_feature) | **GET** /featuretable/feature/{featureId} | Retrieve a specific Feature based on its ID
[**retrieve_feature_ion_ms_spectra**](FeaturetableApi.md#retrieve_feature_ion_ms_spectra) | **GET** /featuretable/feature/{featureId}/ms | Retrieve Feature Ion MS Spectra
[**retrieve_feature_ms_ms_spectra**](FeaturetableApi.md#retrieve_feature_ms_ms_spectra) | **GET** /featuretable/feature/{featureId}/msms | Retrieve Feature MS/MS Spectra
[**retrieve_feature_ms_ms_spectra_deiso**](FeaturetableApi.md#retrieve_feature_ms_ms_spectra_deiso) | **GET** /featuretable/feature/{featureId}/msmsdeiso | Retrieve Feature MS/MS Deisotoped Spectra
[**retrieve_feature_ms_spectra_details**](FeaturetableApi.md#retrieve_feature_ms_spectra_details) | **GET** /featuretable/feature/{featureId}/ms/details | Retrieve Feature MS Spectra Details
[**retrieve_feature_table**](FeaturetableApi.md#retrieve_feature_table) | **GET** /featuretable/{featureTableId} | Fetches a specific Feature Table based on its ID
[**retrieve_intensity_matrix**](FeaturetableApi.md#retrieve_intensity_matrix) | **GET** /featuretable/intensitymatrix/{featureTableId} | Retrieve a intensity matrix of a Feature Table based on its ID
[**save_new_annotation_configuration**](FeaturetableApi.md#save_new_annotation_configuration) | **POST** /featuretable/{featureTableId}/annotation/configuration/save | Save a new Annotation Configuration for a specific Feature Table

# **add_flag_to_feature**
> add_flag_to_feature(feature_id, flag)

Add Flag to Feature

This operation adds a flag to a specific feature identified by the 'featureId' path parameter.

### Example
```python
from __future__ import print_function
import time
import metaPyScape
from metaPyScape.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = metaPyScape.FeaturetableApi()
feature_id = 'feature_id_example' # str | The unique identifier of the feature to which the flag is to be added.
flag = 'flag_example' # str | The flag to be added to the feature.

try:
    # Add Flag to Feature
    api_instance.add_flag_to_feature(feature_id, flag)
except ApiException as e:
    print("Exception when calling FeaturetableApi->add_flag_to_feature: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **feature_id** | **str**| The unique identifier of the feature to which the flag is to be added. | 
 **flag** | **str**| The flag to be added to the feature. | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_annotation**
> create_annotation(body, feature_id)

Create a custom annotation for a specific feature

With this operation, an annotation from any custom annotation outside of MetaboScape can be created for a Feature with a given 'featureId'. The 'candidate' parameter specifies the annotation candidate to be created. The annotation tool will be defined as \"External\" in MetaboScape.

### Example
```python
from __future__ import print_function
import time
import metaPyScape
from metaPyScape.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = metaPyScape.FeaturetableApi()
body = metaPyScape.AnnotationCandidate() # AnnotationCandidate | The annotation candidate to be created.
feature_id = 'feature_id_example' # str | The unique identifier of the feature for which the annotation is to be created.

try:
    # Create a custom annotation for a specific feature
    api_instance.create_annotation(body, feature_id)
except ApiException as e:
    print("Exception when calling FeaturetableApi->create_annotation: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AnnotationCandidate**](AnnotationCandidate.md)| The annotation candidate to be created. | 
 **feature_id** | **str**| The unique identifier of the feature for which the annotation is to be created. | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_feature_table**
> ProjectTaskSummary create_feature_table(body)

Create a new Feature Table based on a project file

This operation creates a new Feature Table based on the details provided in the 'projectFile' parameter. The returned data is in JSON format.

### Example
```python
from __future__ import print_function
import time
import metaPyScape
from metaPyScape.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = metaPyScape.FeaturetableApi()
body = 'body_example' # str | The YAML file that references a project and experiment, and defines the structure of one Feature Table. The Project ID and Experiment ID are mandatory to create a Feature Table!

try:
    # Create a new Feature Table based on a project file
    api_response = api_instance.create_feature_table(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FeaturetableApi->create_feature_table: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**str**](str.md)| The YAML file that references a project and experiment, and defines the structure of one Feature Table. The Project ID and Experiment ID are mandatory to create a Feature Table! | 

### Return type

[**ProjectTaskSummary**](ProjectTaskSummary.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: text/plain
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_lipid_species_annotations_with_method**
> list[AnnotationDetails] create_lipid_species_annotations_with_method(body, annotation_method_uuid)

Create Lipid Species Annotations with Method

This operation creates Lipid Species Annotations using a specific method identified by the 'annotationMethodUuid' path parameter.

### Example
```python
from __future__ import print_function
import time
import metaPyScape
from metaPyScape.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = metaPyScape.FeaturetableApi()
body = metaPyScape.AnnotationConfiguration() # AnnotationConfiguration | The configuration for the annotations.
annotation_method_uuid = 'annotation_method_uuid_example' # str | The unique identifier of the method for which the Lipid Species Annotations are to be created.

try:
    # Create Lipid Species Annotations with Method
    api_response = api_instance.create_lipid_species_annotations_with_method(body, annotation_method_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FeaturetableApi->create_lipid_species_annotations_with_method: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AnnotationConfiguration**](AnnotationConfiguration.md)| The configuration for the annotations. | 
 **annotation_method_uuid** | **str**| The unique identifier of the method for which the Lipid Species Annotations are to be created. | 

### Return type

[**list[AnnotationDetails]**](AnnotationDetails.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_smart_formula_annotations_with_method**
> list[AnnotationDetails] create_smart_formula_annotations_with_method(body, annotation_method_uuid)

Create SmartFormula Annotations with Method

This operation creates SmartFormula Annotations using a specific method identified by the 'annotationMethodUuid' path parameter.

### Example
```python
from __future__ import print_function
import time
import metaPyScape
from metaPyScape.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = metaPyScape.FeaturetableApi()
body = [metaPyScape.MainIonDetails()] # list[MainIonDetails] | The main ion details for the annotations.
annotation_method_uuid = 'annotation_method_uuid_example' # str | The unique identifier of the method for which the SmartFormula Annotations are to be created.

try:
    # Create SmartFormula Annotations with Method
    api_response = api_instance.create_smart_formula_annotations_with_method(body, annotation_method_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FeaturetableApi->create_smart_formula_annotations_with_method: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**list[MainIonDetails]**](MainIonDetails.md)| The main ion details for the annotations. | 
 **annotation_method_uuid** | **str**| The unique identifier of the method for which the SmartFormula Annotations are to be created. | 

### Return type

[**list[AnnotationDetails]**](AnnotationDetails.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_target_list_annotations_with_method**
> list[AnnotationDetails] create_target_list_annotations_with_method(body, annotation_method_uuid)

Create Target List Annotations with Method

This operation creates Target List Annotations using a specific method identified by the 'annotationMethodUuid' path parameter.

### Example
```python
from __future__ import print_function
import time
import metaPyScape
from metaPyScape.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = metaPyScape.FeaturetableApi()
body = metaPyScape.AnnotationConfiguration() # AnnotationConfiguration | The configuration for the annotations.
annotation_method_uuid = 'annotation_method_uuid_example' # str | The unique identifier of the method for which the Target List Annotations are to be created.

try:
    # Create Target List Annotations with Method
    api_response = api_instance.create_target_list_annotations_with_method(body, annotation_method_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FeaturetableApi->create_target_list_annotations_with_method: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AnnotationConfiguration**](AnnotationConfiguration.md)| The configuration for the annotations. | 
 **annotation_method_uuid** | **str**| The unique identifier of the method for which the Target List Annotations are to be created. | 

### Return type

[**list[AnnotationDetails]**](AnnotationDetails.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_annotation**
> delete_annotation(feature_id, annotation_id)

Delete a specific annotation for a specific feature

This operation deletes a specific annotation for a specific feature identified by the 'featureId' path parameter. The parameter 'annotationId' determines the annotation to be deleted. Not all annotations for the feature are deleted.

### Example
```python
from __future__ import print_function
import time
import metaPyScape
from metaPyScape.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = metaPyScape.FeaturetableApi()
feature_id = 'feature_id_example' # str | The unique identifier of the feature for which the annotation is to be deleted.
annotation_id = 'annotation_id_example' # str | The unique identifier of the annotation to be deleted.

try:
    # Delete a specific annotation for a specific feature
    api_instance.delete_annotation(feature_id, annotation_id)
except ApiException as e:
    print("Exception when calling FeaturetableApi->delete_annotation: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **feature_id** | **str**| The unique identifier of the feature for which the annotation is to be deleted. | 
 **annotation_id** | **str**| The unique identifier of the annotation to be deleted. | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **generate_new_eics_and_eims**
> generate_new_eics_and_eims(body, feature_table_id)

Generate new EICs and EIMs for a specific Feature Table

This operation generates new Extracted Ion Chromatograms (EICs) and Extracted Ion Mobilograms (EIMs) for a specific Feature Table identified by the 'featureTableId' path parameter. The 'featureIds' parameter specifies the features for which the EICs and EIMs are to be generated.

### Example
```python
from __future__ import print_function
import time
import metaPyScape
from metaPyScape.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = metaPyScape.FeaturetableApi()
body = ['body_example'] # list[str] | The identifiers of the features for which the EICs and EIMs are to be generated.
feature_table_id = 'feature_table_id_example' # str | The unique identifier of the Feature Table for which the EICs and EIMs are to be generated.

try:
    # Generate new EICs and EIMs for a specific Feature Table
    api_instance.generate_new_eics_and_eims(body, feature_table_id)
except ApiException as e:
    print("Exception when calling FeaturetableApi->generate_new_eics_and_eims: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**list[str]**](str.md)| The identifiers of the features for which the EICs and EIMs are to be generated. | 
 **feature_table_id** | **str**| The unique identifier of the Feature Table for which the EICs and EIMs are to be generated. | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_flag_from_feature**
> remove_flag_from_feature(feature_id, flag)

Remove Flag from Feature

This operation removes a flag from a specific feature identified by the 'featureId' path parameter.

### Example
```python
from __future__ import print_function
import time
import metaPyScape
from metaPyScape.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = metaPyScape.FeaturetableApi()
feature_id = 'feature_id_example' # str | The unique identifier of the feature from which the flag is to be removed.
flag = 'flag_example' # str | The flag to be removed from the feature.

try:
    # Remove Flag from Feature
    api_instance.remove_flag_from_feature(feature_id, flag)
except ApiException as e:
    print("Exception when calling FeaturetableApi->remove_flag_from_feature: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **feature_id** | **str**| The unique identifier of the feature from which the flag is to be removed. | 
 **flag** | **str**| The flag to be removed from the feature. | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_annotation_configuration_by_id**
> AnnotationToolConfiguration retrieve_annotation_configuration_by_id(configuration_id)

Retrieve Annotation Configuration by ID

This operation retrieves an Annotation Configuration identified by the 'configurationId' path parameter.

### Example
```python
from __future__ import print_function
import time
import metaPyScape
from metaPyScape.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = metaPyScape.FeaturetableApi()
configuration_id = 'configuration_id_example' # str | The unique identifier of the Annotation Configuration to be retrieved.

try:
    # Retrieve Annotation Configuration by ID
    api_response = api_instance.retrieve_annotation_configuration_by_id(configuration_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FeaturetableApi->retrieve_annotation_configuration_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **configuration_id** | **str**| The unique identifier of the Annotation Configuration to be retrieved. | 

### Return type

[**AnnotationToolConfiguration**](AnnotationToolConfiguration.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_annotation_methods_by_tool_id**
> list[AnnotationMethod] retrieve_annotation_methods_by_tool_id(tool_id)

Retrieve Annotation Methods by Tool ID

This operation retrieves Annotation Methods for a specific tool identified by the 'toolId' path parameter ('TL' for Target List, 'LS' for Lipid Species, 'SL' for Spectral Library, 'SF' for SmartFormula).

### Example
```python
from __future__ import print_function
import time
import metaPyScape
from metaPyScape.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = metaPyScape.FeaturetableApi()
tool_id = 'tool_id_example' # str | The unique identifier of the tool for which the Annotation Methods are to be retrieved. ('TL' for Target List, 'LS' for Lipid Species, 'SL' for Spectral Library, 'SF' for SmartFormula)

try:
    # Retrieve Annotation Methods by Tool ID
    api_response = api_instance.retrieve_annotation_methods_by_tool_id(tool_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FeaturetableApi->retrieve_annotation_methods_by_tool_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tool_id** | **str**| The unique identifier of the tool for which the Annotation Methods are to be retrieved. (&#x27;TL&#x27; for Target List, &#x27;LS&#x27; for Lipid Species, &#x27;SL&#x27; for Spectral Library, &#x27;SF&#x27; for SmartFormula) | 

### Return type

[**list[AnnotationMethod]**](AnnotationMethod.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_eics_for_feature**
> list[FeatureEics] retrieve_eics_for_feature(feature_id)

Retrieve EICs for a specific feature

This operation retrieves Extracted Ion Chromatograms (EICs) for a specific feature identified by the 'featureId' path parameter.

### Example
```python
from __future__ import print_function
import time
import metaPyScape
from metaPyScape.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = metaPyScape.FeaturetableApi()
feature_id = 'feature_id_example' # str | The unique identifier of the feature for which the EICs are to be retrieved.

try:
    # Retrieve EICs for a specific feature
    api_response = api_instance.retrieve_eics_for_feature(feature_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FeaturetableApi->retrieve_eics_for_feature: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **feature_id** | **str**| The unique identifier of the feature for which the EICs are to be retrieved. | 

### Return type

[**list[FeatureEics]**](FeatureEics.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_eims_for_feature**
> list[FeatureEims] retrieve_eims_for_feature(feature_id)

Retrieve EIMs for a specific feature

This operation retrieves Extracted Ion Mobilograms (EIMs) for a specific feature identified by the 'featureId' path parameter.

### Example
```python
from __future__ import print_function
import time
import metaPyScape
from metaPyScape.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = metaPyScape.FeaturetableApi()
feature_id = 'feature_id_example' # str | The unique identifier of the feature for which the EIMs are to be retrieved.

try:
    # Retrieve EIMs for a specific feature
    api_response = api_instance.retrieve_eims_for_feature(feature_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FeaturetableApi->retrieve_eims_for_feature: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **feature_id** | **str**| The unique identifier of the feature for which the EIMs are to be retrieved. | 

### Return type

[**list[FeatureEims]**](FeatureEims.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_feature**
> Feature retrieve_feature(feature_id)

Retrieve a specific Feature based on its ID

This operation retrieves a specific Feature identified by the 'featureId' path parameter. The returned data is in JSON format.

### Example
```python
from __future__ import print_function
import time
import metaPyScape
from metaPyScape.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = metaPyScape.FeaturetableApi()
feature_id = 'feature_id_example' # str | The unique identifier of the Feature to be retrieved.

try:
    # Retrieve a specific Feature based on its ID
    api_response = api_instance.retrieve_feature(feature_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FeaturetableApi->retrieve_feature: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **feature_id** | **str**| The unique identifier of the Feature to be retrieved. | 

### Return type

[**Feature**](Feature.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_feature_ion_ms_spectra**
> list[FeatureIonMsSpectrumInfo] retrieve_feature_ion_ms_spectra(feature_id)

Retrieve Feature Ion MS Spectra

This operation retrieves a consensus MS Spectrum for every ion of a Feature identified by the 'featureId' path parameter.

### Example
```python
from __future__ import print_function
import time
import metaPyScape
from metaPyScape.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = metaPyScape.FeaturetableApi()
feature_id = 'feature_id_example' # str | The unique identifier of the feature for which the Feature Ion MS Spectra are to be retrieved.

try:
    # Retrieve Feature Ion MS Spectra
    api_response = api_instance.retrieve_feature_ion_ms_spectra(feature_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FeaturetableApi->retrieve_feature_ion_ms_spectra: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **feature_id** | **str**| The unique identifier of the feature for which the Feature Ion MS Spectra are to be retrieved. | 

### Return type

[**list[FeatureIonMsSpectrumInfo]**](FeatureIonMsSpectrumInfo.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_feature_ms_ms_spectra**
> list[FeatureIonMsMsSpectrumInfo] retrieve_feature_ms_ms_spectra(feature_id)

Retrieve Feature MS/MS Spectra

This operation retrieves an MS/MS spectrum (if available) for every ion of a specific feature identified by the 'featureId' path parameter.

### Example
```python
from __future__ import print_function
import time
import metaPyScape
from metaPyScape.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = metaPyScape.FeaturetableApi()
feature_id = 'feature_id_example' # str | The unique identifier of the feature for which the Feature MS/MS Spectra are to be retrieved.

try:
    # Retrieve Feature MS/MS Spectra
    api_response = api_instance.retrieve_feature_ms_ms_spectra(feature_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FeaturetableApi->retrieve_feature_ms_ms_spectra: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **feature_id** | **str**| The unique identifier of the feature for which the Feature MS/MS Spectra are to be retrieved. | 

### Return type

[**list[FeatureIonMsMsSpectrumInfo]**](FeatureIonMsMsSpectrumInfo.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_feature_ms_ms_spectra_deiso**
> list[FeatureIonMsMsSpectrumInfo] retrieve_feature_ms_ms_spectra_deiso(feature_id)

Retrieve Feature MS/MS Deisotoped Spectra

This operation retrieves a deisotoped MS/MS spectrum (if available) for every ion of a specific feature identified by the 'featureId' path parameter.

### Example
```python
from __future__ import print_function
import time
import metaPyScape
from metaPyScape.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = metaPyScape.FeaturetableApi()
feature_id = 'feature_id_example' # str | The unique identifier of the feature for which the Feature MS/MS Deisotoped Spectra are to be retrieved.

try:
    # Retrieve Feature MS/MS Deisotoped Spectra
    api_response = api_instance.retrieve_feature_ms_ms_spectra_deiso(feature_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FeaturetableApi->retrieve_feature_ms_ms_spectra_deiso: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **feature_id** | **str**| The unique identifier of the feature for which the Feature MS/MS Deisotoped Spectra are to be retrieved. | 

### Return type

[**list[FeatureIonMsMsSpectrumInfo]**](FeatureIonMsMsSpectrumInfo.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_feature_ms_spectra_details**
> list[FeatureIonMsSpectrumInfo] retrieve_feature_ms_spectra_details(feature_id)

Retrieve Feature MS Spectra Details

This operation retrieves MS Spectra for every analysis of a specific Feature identified by the 'featureId' parameter.

### Example
```python
from __future__ import print_function
import time
import metaPyScape
from metaPyScape.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = metaPyScape.FeaturetableApi()
feature_id = 'feature_id_example' # str | The unique identifier of the feature for which the Feature MS Spectra Details are to be retrieved.

try:
    # Retrieve Feature MS Spectra Details
    api_response = api_instance.retrieve_feature_ms_spectra_details(feature_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FeaturetableApi->retrieve_feature_ms_spectra_details: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **feature_id** | **str**| The unique identifier of the feature for which the Feature MS Spectra Details are to be retrieved. | 

### Return type

[**list[FeatureIonMsSpectrumInfo]**](FeatureIonMsSpectrumInfo.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_feature_table**
> list[Feature] retrieve_feature_table(feature_table_id)

Fetches a specific Feature Table based on its ID

This operation fetches a specific Feature Table identified by the 'featureTableId' path parameter. The returned data is in JSON format and contains an array of 'Feature' objects.

### Example
```python
from __future__ import print_function
import time
import metaPyScape
from metaPyScape.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = metaPyScape.FeaturetableApi()
feature_table_id = 'feature_table_id_example' # str | The unique identifier of the Feature Table to be retrieved.

try:
    # Fetches a specific Feature Table based on its ID
    api_response = api_instance.retrieve_feature_table(feature_table_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FeaturetableApi->retrieve_feature_table: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **feature_table_id** | **str**| The unique identifier of the Feature Table to be retrieved. | 

### Return type

[**list[Feature]**](Feature.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_intensity_matrix**
> FeatureMatrix retrieve_intensity_matrix(feature_table_id)

Retrieve a intensity matrix of a Feature Table based on its ID

Retrieve the intensity matrix of a Feature Table (i.e. a 2D array of intensities with dimensions based on the indices of Features and Analyses) identified by the 'featureTableId' path parameter. The returned data is in JSON format.

### Example
```python
from __future__ import print_function
import time
import metaPyScape
from metaPyScape.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = metaPyScape.FeaturetableApi()
feature_table_id = 'feature_table_id_example' # str | The unique identifier of the Feature Table whose intensity matrix is to be retrieved.

try:
    # Retrieve a intensity matrix of a Feature Table based on its ID
    api_response = api_instance.retrieve_intensity_matrix(feature_table_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FeaturetableApi->retrieve_intensity_matrix: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **feature_table_id** | **str**| The unique identifier of the Feature Table whose intensity matrix is to be retrieved. | 

### Return type

[**FeatureMatrix**](FeatureMatrix.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save_new_annotation_configuration**
> str save_new_annotation_configuration(body, feature_table_id)

Save a new Annotation Configuration for a specific Feature Table

This operation saves a new Annotation Configuration for a specific Feature Table identified by the 'featureTableId' path parameter. The 'config' parameter specifies the Annotation Configuration to be saved.

### Example
```python
from __future__ import print_function
import time
import metaPyScape
from metaPyScape.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = metaPyScape.FeaturetableApi()
body = metaPyScape.AnnotationToolConfiguration() # AnnotationToolConfiguration | The Annotation Configuration to be saved.
feature_table_id = 'feature_table_id_example' # str | The unique identifier of the Feature Table for which the Annotation Configuration is to be saved.

try:
    # Save a new Annotation Configuration for a specific Feature Table
    api_response = api_instance.save_new_annotation_configuration(body, feature_table_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FeaturetableApi->save_new_annotation_configuration: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AnnotationToolConfiguration**](AnnotationToolConfiguration.md)| The Annotation Configuration to be saved. | 
 **feature_table_id** | **str**| The unique identifier of the Feature Table for which the Annotation Configuration is to be saved. | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

