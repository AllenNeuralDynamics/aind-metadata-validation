import json
import os
import sys

import pandas as pd

from aind_data_access_api.document_db_ssh import DocumentDbSSHClient, DocumentDbSSHCredentials
import aind_codeocean_api.codeocean as co


region = os.getenv("AWS_SECRET_ACCESS_KEY")

def create_co_client():
    token = os.getenv("CUSTOM_KEY")
    domain = os.getenv("CUSTOM_KEY_2")

    co_client = co.CodeOceanClient(domain=domain, token=token)

    return co_client

def find_unmatched_names(co_client):
    response = co_client.search_all_data_assets()
    results = response.json()['results']

    print(results[:3])

    problem_files = {
        r.get("id"):
        {
            "id": r.get("id"),
            "asset_name": r.get("name"),
            "datadesc_name": r.get("data_description").get("name")
            
        }
        for r in results if r.get("name") != r.get("data_description").get("name")
    }

    return problem_files

def get_co_files(co_client, keys):
    response = co_client.search_all_data_assets()
    results = response.json()['results']

    co_files = {
        r.get("id"):
        {
            "id": r.get("id"),
            "name": r.get("name"),
            "custom_metadata": r.get("custom_metadata")
        }
        for r in results if r.get('id') in keys
    }

    return co_files


def create_doc_db_client():
    DOC_DB_USERNAME = os.getenv("DOC_DB_USERNAME")
    DOC_DB_PASSWORD = os.getenv("DOC_DB_PASSWORD")

    DOC_DB_HOST = os.getenv("DOC_DB_HOST")
    
    DOC_DB_SSH_HOST_PROD = os.getenv("DOC_DB_SSH_HOST_PROD")
    DOC_DB_SSH_USERNAME_PROD = os.getenv("DOC_DB_SSH_USERNAME_PROD")
    DOC_DB_SSH_PASS_PROD = os.getenv("DOC_DB_SSH_PASS_PROD")
    
    DOC_DB_DATABASE = "metadata_index"
    DOC_DB_COLLECTION = "data_assets"

    doc_db_credentials = DocumentDbSSHCredentials(
        host=DOC_DB_HOST,
        username=DOC_DB_USERNAME,
        password=DOC_DB_PASSWORD,
        ssh_host=DOC_DB_SSH_HOST_PROD,
        ssh_username=DOC_DB_SSH_USERNAME_PROD,
        ssh_password=DOC_DB_SSH_PASS_PROD,
        database=DOC_DB_DATABASE,
        collection=DOC_DB_COLLECTION,
    )

    doc_db_client = DocumentDbSSHClient(credentials=doc_db_credentials)
    
    doc_db_client.start()

    return doc_db_client


def get_doc_db_records(doc_db_client, projection=None, filter_query=None):
    """aggregate all relevant docdb files and metadata"""
    
    if not projection:
        projection = {
            "name": 1,
            "created": 1,
            "location": 1,
            "procedures": 1,
            "processing": 1,
            "metadata": 1,
            "rig": 1,
            "data_description": 1,
            "session": 1,
            "acquisition": 1,
            "subject": 1,
        }

    response = list(doc_db_client.collection.find(filter=filter_query, projection=projection))

#     records = {item["_id"]: item for item in response}

    return response


def get_missing_files(all_files):
    
#     all_files = list(doc_store_client.retrieve_data_asset_records())
    
    headers = ["_id", "name", "created", "location"]
    expected_files = ["data_description", "acquisition", "procedures", "subject", "instrument", "processing", "rig", "session", "metadata"]
    presence = []

    extra_files = []
    
    for record in all_files:
        present_files = [key for key in record.keys() if record[key]]
        extra_files = [file for file in present_files if file not in expected_files if file not in extra_files]
        present_files = set(present_files).intersection(expected_files)
        subj = None
        if 'data_description' in present_files:
            if record["data_description"] and 'subject_id' in record["data_description"].keys():
                subj = record["data_description"]['subject_id']

        presence.append(
            [
                *[record[header] for header in headers], subj,
                1 if '_stitched_' in record["name"] else 0,
                *[1 if value in present_files else 0 for value in expected_files]
            ]
        )
    file_presence = pd.DataFrame(presence, columns=[*headers, 'subject_id', "derived", *expected_files])
    file_presence = file_presence.set_index('_id')

    return file_presence

def get_df_totals(presence_df):
    columns = ["data_description", "acquisition", "procedures", "subject", "instrument", "processing", "rig", "session", "metadata"]

    totals = {}
    for col in columns:
        totals[col] = int(presence_df[col].sum())

    totals["total_files"] = len(presence_df)

    return totals




