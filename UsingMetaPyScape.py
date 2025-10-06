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
samples_api = metaPyScape.SamplesApi()

# what is this block exactly for? getting project information, are these two approaches for getting the same information?


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



"""
# getting sample information (--> for metadata ms_run, assay)
# sample information 

try:
    ## A Test featuretableId, hardcoded. change later
    featuretableId = "2c32680e-debc-4f77-8970-78cf547d9875"
    #sampleInfo = samples_api.retrieve_project_info(featuretableId)
    api_response_sample = samples_api.list_all_samples(featuretableId)
    pprint.pp(api_response_sample)
except ApiException as e:
    print("Exception when calling SamplesApi->list_all_samples: %s\n" % e)

#--> this is not working 
"""

# get featuretable information

try:
    # Fetches a specific Feature Table based on its ID
    featuretableId = "2c32680e-debc-4f77-8970-78cf547d9875"
    api_response_ft = featuretable_api.retrieve_feature_table(featuretableId)
    # pprint.pp(api_response_ft)
except ApiException as e:
    print("Exception when calling FeaturetableApi->retrieve_feature_table: %s\n" % e)

# extract information from featuretables as a list 

def get_info_ft(featuretable, list_name, column): 
    """
    takes a featuretable, an empty list, and the name of the wanted column to extract data from as a string
    returns a list with column data for every feature
    """ 
    for feature in featuretable: 
        actual_info = getattr(feature, column)
        list_name.append(actual_info)
    return list_name


#getting information out of featuretable 

mass_list = []
mass = get_info_ft(api_response_ft, mass_list, "mass")

featureId_list = []
featureIds = get_info_ft(api_response_ft, featureId_list, "id")

rt_list = []
rt_values = get_info_ft(api_response_ft, rt_list, "rt_in_seconds")



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