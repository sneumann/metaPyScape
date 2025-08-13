#!/usr/bin/env python3

"""
UsingMetaPyScape
"""

from __future__ import print_function
import metaPyScape
from metaPyScape.rest import ApiException
import yaml
import json

# pymzTab-m
import time
import mztab_m_swagger_client
from mztab_m_swagger_client.rest import ApiException
from mztab_m_swagger_client.models import Metadata
from mztab_m_swagger_client.models import SmallMoleculeSummary
from mztab_m_swagger_client.models import SmallMoleculeFeature
from mztab_m_swagger_client.models import SmallMoleculeEvidence

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
feature_table_api = metaPyScape.FeaturetableApi(api_client)

try:
    api_response = project_api.list_all_projects()
    # print as JSON
    # print(json.dumps(api_response, default=str, indent=2))
except ApiException as e:
    print("Exception when calling Project->list_all_projects: %s\n" % e)

try:
    ## A Test Project
    projectId = "87d912bb-4153-4443-bf2a-1036548a0961"
    projectInfo = project_api.retrieve_project_info(projectId)
    project = project_api.retrieve_project(projectId)
    # Use the first experiment
    experiment = project.experiments[0]
except ApiException as e:
    print("Exception when getting project infos: %s\n" % e)


# featureTablesID=2c32680e-debc-4f77-8970-78cf547d9875

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

mztabfile = mztab_m_swagger_client.MzTab(metadata=mtd, 
                                         small_molecule_summary=sml,
                                         small_molecule_feature=smf,
                                         small_molecule_evidence=sme
                                         )
