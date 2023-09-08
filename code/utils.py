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
        
        if 'session' in record.dict().keys():
            session = record.session
            if 'experimenter_full_name' in session.keys():
                cur_experimenter = session['experimenter_full_name']
                if type(cur_experimenter) == list:
                    experimenters += [*cur_experimenter]
                else:
                    if not pd.isna(cur_experimenter):
                        experimenters += [cur_experimenter]
                        
            
        if 'acquisition' in record.dict().keys():
            acquisition = record.acquisition
            if 'experimenter_full_name' in acquisition.keys():
                cur_experimenter = acquisition['experimenter_full_name']
                if type(cur_experimenter) == list:
                    experimenters += [*cur_experimenter]
                else:
                    if not pd.isna(cur_experimenter):
                        experimenters += [cur_experimenter]
            
        
        for search_zone in ['subject_procedures','specimen_procedures']:
            keys = record.dict().keys()
            if 'procedures' not in keys:
                continue
            if not record.procedures:
                continue
                
            procedures_file = record.procedures
                
            if search_zone not in procedures_file.keys():
                continue
            
            procedure_bucket = procedures_file[search_zone]
            try: 
                if type(procedure_bucket) == list:
                    if len(procedure_bucket) == 0:
                        continue
            except:
                print(procedure_bucket)
                print("couldnt compare size")
            
            try:
                if type(procedure_bucket) != list:
                    if pd.isna(procedure_bucket):
                        continue
            except:
                
                print("something nonetype")
                print(procedures_file)
                
            if len(procedure_bucket) > 0:
                for procedure in procedure_bucket:
                    if 'experimenter_full_name' not in procedure.keys():
                        continue

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
