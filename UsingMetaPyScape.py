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
from mztab_m_swagger_client.models import Parameter


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


# create an instance of the API class for the subsections of MetaboScape REST API 

project_api = metaPyScape.ProjectsApi(api_client)
featuretable_api = metaPyScape.FeaturetableApi(api_client)
samples_api = metaPyScape.SamplesApi(api_client)
#ccs_api = metaPyScape.CcspredictApi(api_client)


#GET a list of all projects in one MetaboScape instance

try:
    api_response_project = project_api.list_all_projects()
except ApiException as e:
    print("Exception when calling Project->list_all_projects: %s\n" % e)

#projectId = api_response_project[0].id                          # take the first project out of the list of projects
projectId = "87d912bb-4153-4443-bf2a-1036548a0961"

#GET information for defined project based on projectId

try:
    projectInfo = project_api.retrieve_project_info(projectId)          
    project = project_api.retrieve_project(projectId)
except ApiException as e:
    print("Exception when getting project infos: %s\n" % e)


experiment = project.experiments[0]                             # Use the first experiment of the project
featuretable_info = experiment.feature_tables[0]                # Use the first featuretable of the experiment
#featuretableId = featuretable_info.id                           # define the featuretableId 
featuretableId = "2c32680e-debc-4f77-8970-78cf547d9875"

# GET sample information for samples of defined featuretable based on featuretableId

try:   
    api_response_sample = samples_api.list_all_samples(featuretableId)
except ApiException as e:
    print("Exception when calling SamplesApi->list_all_samples: %s\n" % e)


# get featuretable data and intensity matrix for defined featuretable based on featuretableId

try:
    api_response_ft = featuretable_api.retrieve_feature_table(featuretableId)
    api_response_intensity = featuretable_api.retrieve_intensity_matrix(featuretableId)         # of type class 'metaPyScape.models.feature_matrix.FeatureMatrix'
except ApiException as e:
    print("Exception when calling FeaturetableApi->retrieve_feature_table: %s\n" % e)


## block for used functions 

# extract information from featuretables as a list 

def get_data(data_list, list_name, column): 
    """
    takes a data_list, an empty list, and the name of the APi endpoint of interest to extract data from as a string
    returns the given list with column data for every entry of original list
    """
    for entry in data_list: 
        actual_info = getattr(entry, column)
        list_name.append(actual_info)
    return list_name

# built a function and then do a for loop over the function: 

def get_sample_intensity(intensities, sample_nr):
    """
    takes the intensity matrix and a sample number as input, returns a list with intensity values for the given sample number 
    """
    sample_data = []
    for feature in intensities: 
        sample_data.append(feature[sample_nr])
    return sample_data

# extract nested information from featuretables as a list

def get_data_SML(api_response_ft, list_name, column_1, column_2):
    """
    takes a data_list, an empty list, and the name of two nested columns to extract data from as strings
    """
    for feature in api_response_ft: 
        if getattr(feature, column_1) is None:
            list_name.append("null")
        else:                                                      
            value = getattr(getattr(feature, column_1), column_2)
            list_name.append(value)                                     
    return list_name 

## collect information for mzTab-M metadata 

# data about experimental design: ms_run, assay 

# actual test file: 18 samples stored in one official MetaboScape REST API sample, 
# --> define first_sample and get analysis info from there

first_sample = api_response_sample[0]                           # contains all 18 samples of the feature table in test project (source comparison IPB data)
sample_info = first_sample.analysis                             # sample_info is a list, each entry in the list has type metaPyScape.models.analysis.Analysis

sampleIds_list = []
sample_Ids = get_data(sample_info, sampleIds_list, "id")        # list of sample Ids

sample_names_list = []
sample_names = get_data(sample_info, sample_names_list, "name") # list of sample names

# build lists of nested dicts (one per sample)
ms_run_entries = []
assay_entries = []

# loop over sample Ids and names to build ms_run and assay entries

for idx, (sid, sname) in enumerate(zip(sample_Ids, sample_names), start=1):
    msrun = {
        "elementType": "MsRun",
        "id": idx,
        "elementType": "element_type",
        "name": None,
        # put the mzML location if you have it; else leave None
        "location": None,
        "instrument_ref": None,
        "format": None,
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

# id_confidence_measure: list of aq scores 
# define Parameter (CV) objects for each aq score 

cv_aq1_mz = Parameter(cv_label= None, cv_accession= None , name="mz_aq_score", value=None)
cv_aq2_rt = Parameter(cv_label= None, cv_accession= None , name="rt_aq_score", value=None)
cv_aq3_iso = Parameter(cv_label= None, cv_accession= None , name="isotope_pattern_aq_score", value=None)
cv_aq4_msms = Parameter(cv_label= None, cv_accession= None , name="msms_aq_score", value=None)
cv_aq5_ccs = Parameter(cv_label= None, cv_accession= None , name="ccs_aq_score", value=None)
cv_aq6_mzdevi = Parameter(cv_label= None, cv_accession= None , name="mz_deviation", value=None)
cv_aq7_rtdevi = Parameter(cv_label= None, cv_accession= None , name="rt_deviation", value=None)
cv_aq8_isoscore = Parameter(cv_label= None, cv_accession= None , name="isotope_pattern_score", value=None)
cv_aq9_msmsscore = Parameter(cv_label= None, cv_accession= None , name="msms_score", value=None)
cv_aq10_ccsdevi = Parameter(cv_label= None, cv_accession= None , name="ccs_deviation", value=None)
cv_aq11_annomod = Parameter(cv_label= None, cv_accession= None , name="annotation_modifiers", value=None)

aq_scores = [cv_aq1_mz, cv_aq2_rt, cv_aq3_iso, cv_aq4_msms, cv_aq5_ccs, cv_aq6_mzdevi, cv_aq7_rtdevi, cv_aq8_isoscore, cv_aq9_msmsscore, cv_aq10_ccsdevi, cv_aq11_annomod]


## collect information for mzTab-M SML, SMF and SME 

# getting intensity values for every sample 

intensities = api_response_intensity.intensities 


# store the intensity data in a dictionary for all samples 
# the list of sample numbers can be dynamic according to the number of samples (change later)

#sample_numbers = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]     # hardcoded for 18 samples
sample_numbers = list(range(1, len(sample_names) + 1))              # dynamic according to number of samples 
intensity_data = {}                                                 

# loop over sample numbers and get intensity data for each sample
# make a dictionary with abundance_assay[sample_nr] as key and intensity list as value 

for sample_nr in sample_numbers: 
    variable_name = f'abundance_assay[{sample_nr+1}]'
    intensity_data[variable_name] = get_sample_intensity(intensities, sample_nr)


# transform the dictionary to a df containing intensity data. 

intensities_df = pd.DataFrame(data=intensity_data)

#make a list of the mz values 
exp_mass_to_charge_list = []

for feature in api_response_ft: 
    #actual_mass_to_charge = feature.featureIons[0].mz              # grap the mz value of the first feature ion 
    exp_mass_to_charge_list.append(feature.feature_ions[0].mz)


#collect feature information as lists 

mass_list = []
mass = get_data(api_response_ft, mass_list, "mass")                 # list of mass values (not used in mzTab-M) 

featureId_list = []
featureIds = get_data(api_response_ft, featureId_list, "id")        # list of feature Ids

rt_list = []
rt_values = get_data(api_response_ft, rt_list, "rt_in_seconds")     # list of rt values

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

adduct_ion = []
for feature in api_response_ft: 
    #actual_adduct_ion = feature.featureIons[0].ion_notation         # grap the name of the first feature ion 
    adduct_ion.append(feature.feature_ions[0].ion_notation)

ccs = []
for feature in api_response_ft: 
    #actual_adduct_ion = feature.featureIons[0].ion_notation         #grap the name of the first feature ion 
    ccs.append(feature.feature_ions[0].ccs)



# make a SML dictionary and dataframe with structure of mzTab-M SML and SMF tables

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



## create mzTab-M sections one by one 
## pymzTab-m
##

# create Metadata object

MTD = Metadata(
    prefix='MTD', 
    mz_tab_version="2.0.0-M", 
    mz_tab_id=featuretable_info.id,
    title=featuretable_info.name, 
    description=projectInfo.description,                            # das passt nicht bzw kommt aus der project_info und ist nciht spezifisch für die featuretable 
    sample_processing=featuretable_info.processing_workflow, 
    instrument=None, 
    software="MetaboScape", 
    publication=None, 
    contact=projectInfo.owner, 
    uri=None, 
    external_study_uri=None, 
    quantification_method="label-free",                             # woher soll die kommen? 
    study_variable="undefined",                                     
    ms_run=ms_run_entries, 
    assay=assay_entries,                                            # "ms_run_ref": ms_run_pre}, how do i implement ms_run_ref the right way? 
    sample=None, 
    custom=None, 
    cv="notNone", 
    database="inhouse ?", 
    derivatization_agent=None, 
    small_molecule_quantification_unit="notNone", 
    small_molecule_feature_quantification_unit="notNone", 
    small_molecule_identification_reliability=None, 
    id_confidence_measure=aq_scores,                                # list of the aq scores? 
    colunit_small_molecule=None, 
    colunit_small_molecule_feature=None, 
    colunit_small_molecule_evidence=None
)

abundance_cols = [f'abundance_assay[{i}]' for i in range(1, 19)]    # define abundance assay columns dynamically according to number of samples

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
        abundance_assay=[row[col] for col in abundance_cols],       # make a list of values from all samples for each row, each row represents one feature
        abundance_study_variable=None,
        abundance_variation_study_variable=None,
        opt= {"identifier": "global_ccs", "param": None, "value": row['opt_ccs']},
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
        abundance_assay=[row[col] for col in abundance_cols],                 # how can i put every abundance assay column here? 
        opt= {"identifier": "global_ccs", "param": None, "value": row['opt_ccs']},
        comment=None
    ),
    axis=1
).tolist()


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

# create the MzTab object

mztab = MzTab(metadata=MTD, 
              small_molecule_summary=SML,
              small_molecule_feature=SMF,
              small_molecule_evidence=SME, 
              )


# write the mztab JSON to file /tmp/mztab.json
with open("example_SMF.json", "w") as f:
  print(mztab, file=f)
  
try:
    writeMzTabM("example_SMF.json", mztab)
except Exception as e:
    print("Error writing MzTab-M file: %s\n" % e)
