#!/usr/bin/env python3

"""
UsingMetaPyScape
"""

from __future__ import print_function

from mztab_m_io.mztab_m_writer import writeMzTabM
import metaPyScape
from metaPyScape.rest import ApiException
import yaml

# pymzTab-m
import mztab_m_swagger_client
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
except ApiException as e:
    print("Exception when getting project infos: %s\n" % e)



# getting sample information (--> for metadata ms_run, assay)
# sample information 

try:
    ## A Test featuretableId, hardcoded. change later
    featuretableId = "2c32680e-debc-4f77-8970-78cf547d9875"
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

#print(api_response_intensity.intensities[0])
#print(type(api_response_intensity.intensities[0]))

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

sample_numbers = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
intensity_data = {}

for sample_nr in sample_numbers: 
    variable_name = f'abundance_assay[{sample_nr}]'
    intensity_data[variable_name] = get_sample_intensity(intensities, sample_nr)

# --> a dictionary can be easily transformed do a df with: 

# intensities_df = pd.DataFrame(data=intensity_data)

#make a list of the mz values (dont know if this is fine, because a feature could have several feature ions)
exp_mass_to_charge = []

for feature in api_response_ft: 
    #actual_mass_to_charge = feature.featureIons[0].mz         #grap the mz value of the first feature ion 
    exp_mass_to_charge.append(feature.featureIons[0].mz)


#make a list of adduct ion for SMF,SME table
adduct_ion = []

for feature in api_response_ft: 
    #actual_adduct_ion = feature.featureIons[0].ion_notation         #grap the name of the first feature ion 
    adduct_ion.append(feature.featureIons[0].ion_notation)

"""
#make a list of adduct ions for SML table
adduct_ions = []

for feature in api_response_ft: 
    #actual_adduct_ion = feature.featureIons[0].ion_notation         #grap the names of all feature ions
    feature_ions = []
    adduct_ions.append(feature.featureIons.ion_notation)
"""

# make a list of chemical names 
chemical_name = []

for feature in api_response_ft: 
    if feature.primaryAnnotation == "null":     
        chemical_name.append("null")
    else:        #grap the chemical name of the primary annotation and add to list of chemical names 
        chemical_name.append(feature.primaryAnnotation.name)

# make a list of chemical formulas
chemical_formula = []

for feature in api_response_ft: 
    if feature.primaryAnnotation == "null":     
        chemical_formula.append("null")
    else:        #grap the chemical name of the primary annotation and add to list of chemical names 
        chemical_formula.append(feature.primaryAnnotation.formula) 





# dataframe wäre hilfreich --> pandas 

"""
##
## pymzTab-m
##

mtd = Metadata(
    prefix='MTD', 
    mz_tab_version="2.0.0-M", 
    mz_tab_id=experiment.id,
    title=projectInfo.name, 
    description=projectInfo.description, 
    sample_processing="standard protocols", 
    instrument=None, 
    software="MetaboScape", 
    publication=None, 
    contact=projectInfo.owner, 
    uri=None, 
    external_study_uri=None, 
    quantification_method="label-free", 
    study_variable="notNone", 
    ms_run="notNone", 
    assay="notNone", 
    sample=None, 
    custom=None, 
    cv="notNone", 
    database="inhouse ?", 
    derivatization_agent=None, 
    small_molecule_quantification_unit="notNone", 
    small_molecule_feature_quantification_unit="notNone", 
    small_molecule_identification_reliability=None, 
    id_confidence_measure="notNone" , 
    colunit_small_molecule=None, 
    colunit_small_molecule_feature=None, 
    colunit_small_molecule_evidence=None
)

sml = [
    SmallMoleculeSummary(
    prefix='SML', header_prefix='SMH', 
    sml_id="notNone", 
    smf_id_refs=None, 
    database_identifier=None, 
    chemical_formula=None, smiles=None, inchi=None, 
    chemical_name=None, uri=None, 
    theoretical_neutral_mass=None, adduct_ions=None, reliability=None, 
    best_id_confidence_measure=None, best_id_confidence_value=None, 
    abundance_assay=None, 
    abundance_study_variable=None, 
    abundance_variation_study_variable=None, 
    opt=None, comment=None)
]

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

sme = [
    SmallMoleculeEvidence(
        prefix='SME', header_prefix='SEH', 
        sme_id="notNone", 
        evidence_input_id="notNone", 
        database_identifier="notNone", 
        chemical_formula=None, smiles=None, inchi=None, chemical_name=None, 
        uri=None, derivatized_form=None, adduct_ion=None, 
        exp_mass_to_charge="notNone", charge="notNone", 
        theoretical_mass_to_charge="notNone", spectra_ref="notNone", 
        identification_method="notNone", ms_level="notNone", 
        id_confidence_measure=None, rank=1, 
        opt=None, comment=None
    )    
]

mztab = MzTab(metadata=mtd, 
              small_molecule_summary=sml,
              small_molecule_feature=smf,
              small_molecule_evidence=sme
              )

# write the mztab JSON to file /tmp/mztab.json
with open("/tmp/mztab.json", "w") as f:
  print(mztab, file=f)
  
try:
    writeMzTabM("/tmp/mzTab-M.json", mztab)
except Exception as e:
    print("Error writing MzTab-M file: %s\n" % e)
"""