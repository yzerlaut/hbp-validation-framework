import numpy as np
from django.core.management.base import BaseCommand

## KG Model Database
import os
from fairgraph.client import KGClient
from fairgraph.base import as_list
from fairgraph.brainsimulation import ModelProject
token = os.environ["HBP_token"]
#nexus_endpoint = "https://nexus-int.humanbrainproject.org/v0"
nexus_endpoint = "https://nexus.humanbrainproject.org/v0"
client = KGClient(token, nexus_endpoint=nexus_endpoint)

from fairgraph.base import KGQuery
# from fairgraph.minds import Dataset
# from fairgraph.core import Person, Activity, AgeCategory, Dataset, EmbargoStatus, Method, Person, Project, Sample, Sex, Species
from fairgraph.minds import Person

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
    


def fetch_KG_database():

    KG_db = {}
    # for label, quant in zip(['Activity', 'AgeCategory', 'Dataset', 'EmbargoStatus', 'Method', 'Person', 'Project', 'Sample', 'Sex', 'Species'],
    #                         [Activity, AgeCategory, Dataset, EmbargoStatus, Method, Person, Project, Sample, Sex, Species]):
    for label, quant in zip(['Person'],
                            [Person]):
        KG_db[label] = {'names':[], 'id':[]}
        db_list = quant.list(client, size=2)
        print(db_list)
        # for entry in db_list:
        #     print(entry)
        #     KG_db[label]['names'].append(entry.name)
        #     KG_db[label]['id'].append(entry.id)
        # print('%i entries for %s' % (len(KG_db[label]['id']), label))
        # KG_db[label]['names'] = np.array(KG_db[label]['names'], dtype=str)
        # KG_db[label]['id'] = np.array(KG_db[label]['id'], dtype=str)
        
    # activity_list = Activity.list(client, size=1000000)
    # for label, quant in zip(['Methods', 'Protocols'],
    #                         [methods, protocols]):
    #     KG_db[label] = {'names':[], 'id':[]}
        
    #     # for act in activity_list:
    #     #     method_list = act.methods.resolve(client)
    #     #     for method in method_list
    #     for entry in db_list:
    #         KG_db[label]['names'].append(entry.name)
    #         KG_db[label]['id'].append(entry.id)
    #     print('%i entries for %s' % (len(KG_db[label]['id']), label))
    #     KG_db[label]['names'] = np.array(KG_db[label]['names'], dtype=str)
    #     KG_db[label]['id'] = np.array(KG_db[label]['id'], dtype=str)
        
    return KG_db

def load_local_db():

    db = dict(np.load('KG_db.npz', allow_pickle=True))
    KG_db = {}
    for key in db.keys():
        KG_db[key] = db[key].item()
    return KG_db

class Command(BaseCommand):
    
    def handle(self, *args, **options):

        KG_db = fetch_KG_database()
        # np.savez('KG_db.npz', **KG_db)

        # KG_db = load_local_db()
        # for name in KG_db['Person']['names']:
        #     if len(name.split('Freund'))>1:
        #         print(name)
        # from fairgraph.minds import Dataset, Person, Brain
        # person_list = Person.list(client, size=100000)
        # author_list1 = [author.name for author in person_list]
        # author_list2 = []
        # dataset_list = Dataset.list(client, size=10000)
        # for dataset in dataset_list:
        #     c_list = dataset.contributors
        #     for contributor in c_list:
        #         print(contributor.resolve(client).name)
        #         author_list2.append(contributor.resolve(client).name)
        # print(len(np.unique(author_list1)), len(np.unique(author_list2)))
        # print(len(author_list2), len(np.unique(author_list2)))
        print(KG_db)#['Activity']['names'])
