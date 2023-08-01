import json
import os
import sys

import pandas as pd

from aind_data_access_api.document_store import DocumentStoreCredentials, Client as DsClient


region = os.getenv("AWS_SECRET_ACCESS_KEY")


def generate_doc_store_client():
    doc_store_creds = DocumentStoreCredentials(aws_secrets_name="aind/data/access/api/document_store/read_only")
    doc_store_client = DsClient(credentials=doc_store_creds, collection_name="data_assets")
    return doc_store_client



def get_missing_files(doc_store_client):
    
    all_files = list(doc_store_client.retrieve_data_asset_records())
    
    headers = ["id", "name", "created", "location"]
    expected_files = ["data_description", "acquisition", "procedures", "subject", "instrument", "processing"]
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