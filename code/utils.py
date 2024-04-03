import json
import os
import sys

import pandas as pd

from aind_data_access_api.document_db import MetadataDbClient
import aind_codeocean_api.codeocean as co



region = os.getenv("AWS_SECRET_ACCESS_KEY")

def create_co_client():
    token = os.getenv("CUSTOM_KEY")
    domain = os.getenv("CUSTOM_KEY_2")


    co_client = co.CodeOceanClient(domain=domain, token=token)

    return co_client

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


def get_doc_db_records(filter_query=None):
    """aggregate all relevant docdb files and metadata"""

    DOC_DB_HOST = os.getenv("CUSTOM_KEY_3")
    DOC_DB_DATABASE = "metadata"
    DOC_DB_COLLECTION = "data_assets"

    doc_db_client = MetadataDbClient(host=DOC_DB_HOST, database=DOC_DB_DATABASE, collection=DOC_DB_COLLECTION,)
    
    results = doc_db_client.retrieve_data_asset_records(filter_query=filter_query, paginate=False)

    records = {item._id: item  for item in results}
    
    names = [item._name for item in results]

    return (records, names)


# probably depreciated
def generate_doc_store_client():
    doc_store_creds = DocumentStoreCredentials(aws_secrets_name="aind/data/access/api/document_store/read_only")
    doc_store_client = DsClient(credentials=doc_store_creds, collection_name="data_assets")
    return doc_store_client



def get_missing_files(doc_store_client):
    
    all_files = list(doc_store_client.retrieve_data_asset_records())
    
    headers = ["id", "name", "created", "location"]
    expected_files = ["data_description", "acquisition", "procedures", "subject", "instrument", "processing", "rig", "session"]
    presence = []

    extra_files = []
    
    for record in all_files:
        present_files = record.dict().keys()
        extra_files = [file for file in present_files if file not in expected_files if file not in extra_files]
        present_files = set(present_files).intersection(expected_files)
        subj = None
        if 'data_description' in present_files:
            if 'subject_id' in record.data_description.keys():
                subj = record.data_description['subject_id']

        presence.append(
            [
                *[record.dict()[header] for header in headers], subj,
                1 if '_stitched_' in record.dict()["name"] else 0,
                *[1 if value in present_files else 0 for value in expected_files]
            ]
        )
    file_presence = pd.DataFrame(presence, columns=[*headers, 'subject_id', "derived", *expected_files])
    file_presence = file_presence.set_index('id')

    return file_presence