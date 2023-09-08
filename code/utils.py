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



def get_unique_genotypes(doc_store_client):
    
    all_files = list(doc_store_client.retrieve_data_asset_records())
    
    genotypes = []
    
    for record in all_files:
        keys = record.dict().keys()       
        if 'subject' not in keys:
            continue
        if not record.subject or 'message' in record.subject.keys() or 'genotype' not in record.subject.keys():
            continue
        if pd.isna(record.subject['genotype']):
            continue
        curr_genotype = record.subject['genotype']
        if curr_genotype:
            genotypes += [record.subject['genotype']]
    
    return set(genotypes)


def get_unique_experimenters(doc_store_client):

    all_files = list(doc_store_client.retrieve_data_asset_records())

    experimenters = []

    for record in all_files:
        keys = record.dict().keys()
        if 'procedures' not in keys:
            continue
        if not record.procedures:
            continue
        if 'subject_procedures' not in record.procedures.keys():
            continue
            
        print(record.procedures)
        try: 
            if len(record.procedures['subject_procedures']) < 2:
                if pd.isna(record.procedures['subject_procedures']):
                    continue
                    
        except:
            if pd.isna(record.procedures['subject_procedures']):
                continue
          
        for procedure in record.procedures['subject_procedures']:

            if pd.isna(procedure['experimenter_full_name']):
                continue
            curr_experimenter = procedure['experimenter_full_name']
            if curr_experimenter:
                experimenters += [curr_experimenter]

    return set(experimenters)


def get_unique_alleles(genotypes):
    alleles = []
    for genotype in genotypes:
        for crossing in genotype.split(';'):
            for allele in crossing.split('/'):
                alleles += [allele]
            
    return set(alleles)
