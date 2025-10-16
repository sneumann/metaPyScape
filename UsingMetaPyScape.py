#!/usr/bin/env python3

"""
UsingMetaPyScape
"""

from __future__ import print_function

from mztab_m_io.mztab_m_writer import writeMzTabM
import metaPyScape
from metaPyScape.rest import ApiException
import yaml
import pandas as pd

# pymzTab-m
from mztab_m_swagger_client import ApiClient, Configuration, ValidateApi
from mztab_m_swagger_client.rest import ApiException
from mztab_m_swagger_client.models import MzTab
from mztab_m_swagger_client.models import Metadata
from mztab_m_swagger_client.models import SmallMoleculeSummary
from mztab_m_swagger_client.models import SmallMoleculeFeature
from mztab_m_swagger_client.models import SmallMoleculeEvidence


from mztab_m_io import *

import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
# Reading the configuration from config.yml with keys base_path and api-key

with open("config.yml", "r") as config_file:
    config = yaml.safe_load(config_file)

configuration = metaPyScape.Configuration()
configuration.host = config.get("base_path", "http://localhost")

api_client = metaPyScape.ApiClient(configuration=configuration, 
                                   header_name="api-key", 
                                   header_value=config.get("api-key", None))


project_api = metaPyScape.ProjectsApi(api_client)
featuretable_api = metaPyScape.FeaturetableApi(api_client)
samples_api = metaPyScape.SamplesApi(api_client)
ccs_api = metaPyScape.CcspredictApi(api_client)

# what is this block exactly for? getting project information, are these two approaches for getting the same information?

#right now, this code block is not needed (07.10.)

try:
    api_response_project = project_api.list_all_projects()
    # print as JSON
    # pprint.pp(api_response_project)
except ApiException as e:
    print("Exception when calling Project->list_all_projects: %s\n" % e)


try:
    ## A Test Project
    ## one could get the project id out of api_response instead of hardcoding
    projectId = "87d912bb-4153-4443-bf2a-1036548a0961"
    projectInfo = project_api.retrieve_project_info(projectId)          
    project = project_api.retrieve_project(projectId)
    # Use the first experiment
    experiment = project.experiments[0]
    featuretable_info = experiment.feature_tables[0]
except ApiException as e:
    print("Exception when getting project infos: %s\n" % e)


# getting sample information (--> for metadata ms_run, assay)
# sample information 

try:
    ## A Test featuretableId, hardcoded. change later
    featuretableId = "2c32680e-debc-4f77-8970-78cf547d9875"
    #featuretableld = featuretable_info.id          this is more dynamic 
    api_response_sample = samples_api.list_all_samples(featuretableId)
    #pprint.pp(api_response_sample)
except ApiException as e:
    print("Exception when calling SamplesApi->list_all_samples: %s\n" % e)


#defining the first sample (hardcoded), change later to more dynamic code 

first_sample = api_response_sample[0]       #first_sample is an object of class metaPyScape.models.sample.Sample
sample_info = first_sample.analysis         #sample_info is a list, each entry in the list has type metaPyScape.models.analysis.Analysis


# get featuretable information

try:
    # Fetches a specific Feature Table based on its ID
    featuretableId = "2c32680e-debc-4f77-8970-78cf547d9875"
    api_response_ft = featuretable_api.retrieve_feature_table(featuretableId)
    api_response_intensity = featuretable_api.retrieve_intensity_matrix(featuretableId)         # of type class 'metaPyScape.models.feature_matrix.FeatureMatrix'
    # pprint.pp(api_response_ft)
except ApiException as e:
    print("Exception when calling FeaturetableApi->retrieve_feature_table: %s\n" % e)


# extract information from featuretables as a list 

def get_data(data_list, list_name, column): 
    """
    takes a data_list, an empty list, and the name of the wanted column to extract data from as a string
    returns the given list with column data for every entry of original list
    """
    for entry in data_list: 
        actual_info = getattr(entry, column)
        list_name.append(actual_info)
    return list_name


#getting information out of featuretable and sample_info

mass_list = []
mass = get_data(api_response_ft, mass_list, "mass")

featureId_list = []
featureIds = get_data(api_response_ft, featureId_list, "id")

rt_list = []
rt_values = get_data(api_response_ft, rt_list, "rt_in_seconds")

sampleIds_list = []
sample_Ids = get_data(sample_info, sampleIds_list, "id")

sample_names_list = []
sample_names = get_data(sample_info, sample_names_list, "name")

# build lists of nested dicts (one per sample)
ms_run_entries = []
assay_entries = []

for idx, (sid, sname) in enumerate(zip(sample_Ids, sample_names), start=1):
    msrun = {
        "elementType": "MsRun",
        "id": idx,
        "elementType": "element_type",
        "name": None,
        # put the mzML location if you have it; else leave None
        "location": None,
        "instrument_ref": None,
        "format": {
            "elementType": "Parameter",
            "id": None,
            "elementType": "element_type",
            "cv_label": "MS",
            "cv_accession": "MS:1000584",
            "name": "mzML file",
            "value": None
        },
        "id_format": None,
        "fragmentation_method": None,
        "scan_polarity":  f"{getattr(featuretable_info, 'polarity', None)} scan" if getattr(featuretable_info, 'polarity', None) else None,
        "hash": None,
        "hash_method": None
    }

    assay = {
        "elementType": "Assay",
        "id": idx,
        "elementType": "element_type",
        "name": sname,
        "custom": None,
        "external_uri": None,
        # reference the sample dict (inlined); some writers expect a reference object, but this matches your example
        "sample_ref": None,
        # list of ms_run refs (we put the full ms_run dict inline to match your example)
        "ms_run_ref": [msrun]
    }

    ms_run_entries.append(msrun)
    assay_entries.append(assay)


# getting intensity values for every sample 

intensities = api_response_intensity.intensities


#built a function and then do a for loop over the function: 

def get_sample_intensity(intensities, sample_nr):
    sample_data = []
    for feature in intensities: 
        sample_data.append(feature[sample_nr])
    return sample_data


# store the intensity data in a dictionary for all samples 
# the list of sample numbers can be dynamic according to the number of samples (change later)

sample_numbers = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
intensity_data = {}

for sample_nr in sample_numbers: 
    variable_name = f'abundance_assay[{sample_nr+1}]'
    intensity_data[variable_name] = get_sample_intensity(intensities, sample_nr)

# --> a dictionary can be easily transformed to a df with: 

intensities_df = pd.DataFrame(data=intensity_data)



#make a list of the mz values (dont know if this is fine, because a feature could have several feature ions)
exp_mass_to_charge_list = []

for feature in api_response_ft: 
    #actual_mass_to_charge = feature.featureIons[0].mz         #grap the mz value of the first feature ion 
    exp_mass_to_charge_list.append(feature.feature_ions[0].mz)


#make a list of adduct ion for SMF,SME table
adduct_ion = []

for feature in api_response_ft: 
    #actual_adduct_ion = feature.featureIons[0].ion_notation         #grap the name of the first feature ion 
    adduct_ion.append(feature.feature_ions[0].ion_notation)

ccs = []

for feature in api_response_ft: 
    #actual_adduct_ion = feature.featureIons[0].ion_notation         #grap the name of the first feature ion 
    ccs.append(feature.feature_ions[0].ccs)


"""
#this block is unfinished 
#make a list of adduct ions for SML table
adduct_ions = []

for feature in api_response_ft: 
    #actual_adduct_ion = feature.featureIons[0].ion_notation         #grap the names of all feature ions
    feature_ions = []
    adduct_ions.append(feature.featureIons.ion_notation)
"""

def get_data_SML(api_response_ft, list_name, column_1, column_2):
    for feature in api_response_ft: 

        if getattr(feature, column_1) is None:
            list_name.append("null")
        else:                                                       #grap the chemical name of the primary annotation and add to list of chemical names 
            value = getattr(getattr(feature, column_1), column_2)
            list_name.append(value)                                     
    return list_name 

chemical_name_list = []
chemical_name = get_data_SML(api_response_ft,chemical_name_list,"primary_annotation","name")

chemical_formula_list = []
chemical_formula = get_data_SML(api_response_ft,chemical_formula_list,"primary_annotation","formula")

smiles_list = []
smiles = get_data_SML(api_response_ft,smiles_list,"primary_annotation","structure_smiles")

inchi_list = []
inchi = get_data_SML(api_response_ft,inchi_list,"primary_annotation","structure_inchi")

database_identifiers_list = []
database_identifiers = get_data_SML(api_response_ft,database_identifiers_list,"primary_annotation","database_identifiers")

# #make a list of aq_scores 
# example_feature = api_response_ft[42]
# aq_score_names = list(example_feature.primary_annotation.aq_scores) 

# print(aq_score_names)



#make a SML dictionary and dataframe as it looks like in publication 

SMF_dict = {
    "SFH": ["SMF"] * 937,
    "SMF_ID": featureIds,             # other way: directly use command from earlier to save time 
    "SME_ID_REFS": ["?"] * 937,       # to be completed 
    "SME_ID_REFS_ambiguity_code": ["?"] * 937, 
    "adduct_ion": adduct_ion,
    "isotopomer": ["?"] * 937,
    "exp_mass_to_charge": exp_mass_to_charge_list,
    "charge": ["?"] * 937,            # to be completed, count the + signs in adduct ion if no charge information is available in the REST API?
    "retention_time_in_seconds": rt_values,   # here also maybe add code directly  
    "retention_time_in_seconds_start": ["?"] * 937,
    "retention_time_in_seconds_end": ["?"] * 937 
}

SMF_df = pd.DataFrame(data=SMF_dict)
SMF_df_wi = pd.concat([SMF_df, intensities_df], axis=1)


SML_dict = {
    "SMH": ["SML"] * 937,
    "SML_ID": featureIds, 
    "database_identifier": database_identifiers, 
    "chemical_formula": chemical_formula,
    "smiles": smiles, 
    "inchi": inchi, 
    "chemical_name": chemical_name, 
    "theoretical_neutral_mass": ["?"] * 937, 
    "adduct_ions": adduct_ion, 
    "reliability": ["?"] * 937, 
    "best_id_confidence_measure": ["?"] * 937, 
    "best_id_confidence_value": ["?"] * 937,  
    "abundance_study_variable": ["?"] * 937, 
    "abundance_variation_study_variable": ["?"] * 937, 
    "opt_ccs": ccs, 
    "comment": ["?"] * 937
}

SML_df = pd.DataFrame(data=SML_dict)
SML_df_wi = pd.concat([SML_df, intensities_df], axis=1)

# print(SMF_df_wi)

"""

# store the intensity data in a dictionary for all samples 
# the list of sample numbers can be dynamic according to the number of samples (change later)

sample_numbers = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
intensity_data = {}

for sample_nr in sample_numbers: 
    variable_name = f'abundance_assay[{sample_nr+1}]'
    intensity_data[variable_name] = get_sample_intensity(intensities, sample_nr)

for annotation in all_annotations: 
    {featureID = 
    annotationID = 
    name = 
    formula = 
    MS_spectra_ref = 
    inchi = 
    smiles = 
    database_identifier = }
""" 


##
## pymzTab-m
##

MTD = Metadata(
    prefix='MTD', 
    mz_tab_version="2.0.0-M", 
    mz_tab_id=featuretable_info.id,
    title=featuretable_info.name, 
    description=projectInfo.description,                            #das passt nicht bzw kommt aus der project_info und ist nciht spezifisch für die featuretable 
    sample_processing=featuretable_info.processing_workflow, 
    instrument=None, 
    software="MetaboScape", 
    publication=None, 
    contact=projectInfo.owner, 
    uri=None, 
    external_study_uri=None, 
    quantification_method="label-free",                             #woher soll die kommen? 
    study_variable="undefined",                                     
    ms_run=ms_run_entries, 
    assay=assay_entries,                                   #  "ms_run_ref": ms_run_pre}, how do i implement ms_run_ref the right way? 
    sample=None, 
    custom=None, 
    cv="notNone", 
    database="inhouse ?", 
    derivatization_agent=None, 
    small_molecule_quantification_unit="notNone", 
    small_molecule_feature_quantification_unit="notNone", 
    small_molecule_identification_reliability=None, 
    id_confidence_measure="notNone" ,                               #list of the aq scores? 
    colunit_small_molecule=None, 
    colunit_small_molecule_feature=None, 
    colunit_small_molecule_evidence=None
)

SML = SML_df_wi.apply(
    lambda row: SmallMoleculeSummary(
        prefix='SML',
        header_prefix='SMH',
        sml_id=row['SML_ID'],
        smf_id_refs=None,
        database_identifier=row['database_identifier'],
        chemical_formula=row['chemical_formula'],
        smiles=row['smiles'],
        inchi=row['inchi'],
        chemical_name=row['chemical_name'],
        uri=None,
        theoretical_neutral_mass=None,
        adduct_ions=row['adduct_ions'],
        reliability=None,
        best_id_confidence_measure=None,
        best_id_confidence_value=None,
        abundance_assay=row['abundance_assay[14]'],
        abundance_study_variable=None,
        abundance_variation_study_variable=None,
        opt=row['opt_ccs'],
        comment=None
    ),
    axis=1
).tolist()

SMF = SMF_df_wi.apply(
    lambda row: SmallMoleculeFeature(
        prefix='SMF',
        header_prefix='SFH',
        smf_id=row['SMF_ID'],
        sme_id_refs=None,
        sme_id_ref_ambiguity_code=None,
        adduct_ion=None,                  #actual test line, before: None              adduct_ion=row['adduct_ion'],
        isotopomer=row['isotopomer'],
        exp_mass_to_charge=row['exp_mass_to_charge'],
        charge=row['charge'],
        retention_time_in_seconds=row['retention_time_in_seconds'],
        retention_time_in_seconds_start=None,
        retention_time_in_seconds_end=None,
        abundance_assay=row['abundance_assay[14]'],                 # how can i put every abundance assay column here? 
        opt=None,
        comment=None
    ),
    axis=1
).tolist()

#adduct_ion=None if row['adduct_ion'] == '?' else row['adduct_ion']
"""
#original code block, to be replaced by the dataframe SMF 
smf = [
    SmallMoleculeFeature(
        prefix='SMF', header_prefix='SFH', 
        smf_id="notNone", 
        sme_id_refs=None, sme_id_ref_ambiguity_code=None, 
        adduct_ion=None, isotopomer=None, 
        exp_mass_to_charge=666, charge=1, 
        retention_time_in_seconds=None, retention_time_in_seconds_start=None, retention_time_in_seconds_end=None, 
        abundance_assay=None, 
        opt=None, comment=None)
]

"""

SME = [
    SmallMoleculeEvidence(
        prefix='SME', header_prefix='SEH', 
        sme_id="notNone", 
        evidence_input_id="notNone", 
        database_identifier="notNone", 
        chemical_formula="null", smiles=None, inchi=None, chemical_name=None, 
        uri=None, derivatized_form=None, adduct_ion=None, 
        exp_mass_to_charge="notNone", charge="notNone", 
        theoretical_mass_to_charge="notNone", spectra_ref="notNone", 
        identification_method="notNone", ms_level="notNone", 
        id_confidence_measure=None, rank=1, 
        opt=None, comment=None
    )    
]

mztab = MzTab(metadata=MTD, 
              small_molecule_summary=SML,
              small_molecule_feature=SMF,
              small_molecule_evidence=SME, 
              )

"""
configuration_mzTab = Configuration()
# configuration_mzTab.host = "https://apps.lifs-tools.org/mztabvalidator/rest/v2/validate?level=info&maxErrors=100&semanticValidation=false"
configuration_mzTab.host = "http://localhost"


api_client_mzTab = ApiClient(configuration=configuration_mzTab)
val = ValidateApi(api_client=api_client_mzTab)
res = val.validate_mz_tab_file(mztab)
with open("out.txt", "w") as f:
  print(res, file=f)
"""

# write the mztab JSON to file /tmp/mztab.json
with open("example_SMF.json", "w") as f:
  print(mztab, file=f)
  
try:
    writeMzTabM("example_SMF.json", mztab)
except Exception as e:
    print("Error writing MzTab-M file: %s\n" % e)
