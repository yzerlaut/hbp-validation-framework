import numpy as np
from django.core.management.base import BaseCommand

## KG Model Database
import os
from fairgraph.client import KGClient
from fairgraph.base import as_list
from fairgraph.brainsimulation import ModelProject
token = os.environ["HBP_token"]
nexus_endpoint = "https://nexus-int.humanbrainproject.org/v0" # "https://nexus.humanbrainproject.org/v0"
client = KGClient(token, nexus_endpoint=nexus_endpoint)

from fairgraph.base import KGQuery
from fairgraph.minds import Dataset

def fetch_all_authors_in_KG():

    query = {
        "path": "minds:author / minds:subjects / minds:samples / minds:methods / schema:name",
        "op": "in",
        "value": ["Electrophysiology recording",
                  "Voltage clamp recording",
                  "Single electrode recording",
                  "functional magnetic resonance imaging"]
    }
    context = {
                "schema": "http://schema.org/",
                "minds": "https://schema.hbp.eu/minds/"
    }

    activity_datasets = KGQuery(Dataset, query, context).resolve(client)
    for dataset in activity_datasets:
        print("* " + dataset.name)
    

author_keys = ['by_name', 'cache', 'context', 'delete', 'exists', 'from_kg_instance', 'from_uri', 'from_uuid', 'get_context', 'id', 'instance', 'list', 'name', 'path', 'property_names', 'resolve', 'rev', 'save', 'save_cache', 'type', 'uri_from_uuid', 'uuid']

from fairgraph.minds import Person, Activity, AgeCategory, Dataset, EmbargoStatus, Method, Person, Project, Sample, Sex, Species

def fetch_KG_database():

    KG_db = {}
    for label, quant in zip(['Activity', 'AgeCategory', 'Dataset', 'EmbargoStatus', 'Method', 'Person', 'Project', 'Sample', 'Sex', 'Species'],
                            [Activity, AgeCategory, Dataset, EmbargoStatus, Method, Person, Project, Sample, Sex, Species]):
        KG_db[label] = {'names':[], 'id':[]}
        db_list = quant.list(client, size=1000000)
        for entry in db_list:
            KG_db[label]['names'].append(entry.name)
            KG_db[label]['id'].append(entry.id)

        KG_db[label]['names'] = np.array(KG_db[label]['names'], dtype=str)
        KG_db[label]['id'] = np.array(KG_db[label]['id'], dtype=str)
                            
    return KG_db

class Command(BaseCommand):
    
    def handle(self, *args, **options):

        KG_db = fetch_KG_database()

        np.savez('KG_db.npz', **KG_db)


