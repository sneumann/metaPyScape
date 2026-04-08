Test fixtures for mtbsccli unit tests
======================================

These JSON files represent example REST API responses from a MetaboScape
server.  They are used in unit tests so that the server is not required to
run the test suite.

How to (re-)generate fixture files
-----------------------------------
Connect to a live MetaboScape instance and run the following commands,
substituting real UUIDs for ``<project-id>`` and ``<featuretable-id>``:

.. code-block:: bash

    # Discover projects and feature tables
    mtbsccli -o json get projects > test/fixtures/projects.json

    # Retrieve a single project (replace UUID as needed)
    mtbsccli -o json get project <project-id> > test/fixtures/project.json

    # Retrieve project task/workflow info
    mtbsccli -o json get project-info <project-id> > test/fixtures/project_info.json

    # Retrieve the feature table (list of features with annotations)
    mtbsccli -o json get featuretable <featuretable-id> > test/fixtures/featuretable.json

    # Retrieve sample / analysis metadata
    mtbsccli -o json get samples <featuretable-id> > test/fixtures/samples.json

    # Retrieve the intensity matrix
    mtbsccli -o json get intensity-matrix <featuretable-id> > test/fixtures/intensity_matrix.json

Files
-----
projects.json         List[Project]      – output of list_all_projects()
project.json          Project            – output of retrieve_project()
project_info.json     ProjectInfo        – output of retrieve_project_info()
featuretable.json     List[Feature]      – output of retrieve_feature_table()
samples.json          List[Sample]       – output of list_all_samples()
intensity_matrix.json FeatureMatrix      – output of retrieve_intensity_matrix()

The bundled files are minimal synthetic stubs covering two features and two
analysis runs.  Replace them with real data for integration-style tests.
