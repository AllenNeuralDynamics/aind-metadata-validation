""" top level run script """
from aind_codeocean_api.codeocean import CodeOceanClient
from aind_codeocean_api.credentials import CodeOceanCredentials

import json
import os
import sys

creds = CodeOceanCredentials().credentials

co_client = CodeOceanClient(domain=creds['domain'], token=creds['token'])

files = co_client.search_all_data_assets()


def get_missing_files(self):
    headers = ["id", "name", "created", "location"]
    expected_files = ["data_description", "acquisition", "procedures", "subject", "instrument", "processing"]
    presence = []
    for record in to_fix:
        subj = record.data_description['subject_id']
        present_files = record.dict().keys()
        present_files = set(present_files).intersection(expected_files)
        presence.append(
            [
                *[record.dict()[header] for header in headers],
                subj,
                1 if 'stitched' in record.dict()["name"] else 0,
                *[1 if value in present_files else 0 for value in expected_files]
            ]
        )
    file_presence = pd.DataFrame(presence, columns=[*headers, 'subject_id', "derived", *expected_files])
    return file_presence


if __name__ == "__main__": run()