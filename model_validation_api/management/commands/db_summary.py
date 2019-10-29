import numpy as np

## Django model database
from ...models import ScientificModel
from django.core.management.base import BaseCommand

## KG Model Database
import os
from fairgraph.client import KGClient
from fairgraph.base import as_list
from fairgraph.brainsimulation import ModelProject
token = os.environ["HBP_token"]
nexus_endpoint = "https://nexus-int.humanbrainproject.org/v0" # "https://nexus.humanbrainproject.org/v0"
client = KGClient(token, nexus_endpoint=nexus_endpoint)


def fetch_djando_db_entries():

    keys = ['abstraction_level', 'alias', 'author',
            'brain_region', 'cell_type', 'code_format', 'creation_date',
            'description', 'id',
            'license', 'model_scope', 'model_type', 'name',
            'organization', 'owner', 'project', 'species']

    
    models = ScientificModel.objects.all()
    data = {}
    for key in keys:
        data[key] = []
        
    for i, model in enumerate(models):
        for key in keys:
            exec('data[key].append(model.'+key+')')

    np.savez('/home/yzerlaut/Desktop/Model-Catagol-DB.npz', **data)
    exec('data = {}')

    
def fetch_kg_entries():

    keys = ['abstraction_level', 'alias', 'authors', 'authors_str', 'brain_region', 'celltype', 'collab_id', 'context', 'date_created', 'description', 'id', 'instance', 'instances', 'list', 'model_of', 'name', 'old_uuid', 'organization', 'owners', 'species', 'uri_from_uuid', 'uuid']
    
    data = {}
    for key in keys:
        data[key] = []
        
    for i, project in enumerate(ModelProject.list(client, size=10000)):
        for key in keys:
            exec('data[key].append(project.'+key+')')

    np.savez('/home/yzerlaut/Desktop/Model-Catagol-KG.npz', **data)
        

def load_data():    
    data_spreadsheet = dict(np.load('/home/yzerlaut/Desktop/Model-Catagol-Spreadsheet.npz', allow_pickle=True))
    data_spreadsheet['name'] = data_spreadsheet['Name']
    data_DB = dict(np.load('/home/yzerlaut/Desktop/Model-Catagol-DB.npz', allow_pickle=True))
    data_KG = dict(np.load('/home/yzerlaut/Desktop/Model-Catagol-KG.npz', allow_pickle=True))
    return data_spreadsheet, data_DB, data_KG


def find_missing_ones():
    data_spreadsheet, data_DB, data_KG = load_data()
    key_ss, key_db, key_kg = list(data_spreadsheet.keys()), list(data_DB.keys()), list(data_KG.keys())
    i_not_in_kg, i_not_in_ss = [], []
    for i_db, name in enumerate(data_DB['name']):
        i_ss = np.argwhere(data_spreadsheet['name']==name).flatten()
        i_kg = np.argwhere(data_KG['name']==name).flatten()
        if (len(i_ss)==0) or (len(i_kg)==0):
            # print('--------------------\nModel:', name)
            if (len(i_ss)==0):
                i_not_in_ss += i_ss
                # print('X) No entry in the spreadsheet')
            if (len(i_kg)==0):
                i_not_in_kg.append(i_db)
                # print('X) No entry in the KG')
    for i_db in i_not_in_kg:
        print('--------------------\n', data_DB['name'][i_db])
        for key in key_db:
            print(data_DB[key][i_db])
    print(len(i_not_in_kg), len(data_KG['name']), len(data_DB['name']))
    print(len(np.unique(data_KG['name'])), len(np.unique(data_DB['name'])))
    

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        # fetch_djando_db_entries()
        fetch_kg_entries()
        

        # models = ScientificModel.objects.all()
        # for m, model in enumerate(models):
        #     print('----------------------\n%i) Model "%s"' % (m, model.name))
        #     try:
        #         for i, instance in enumerate(model.instances.all()):
        #             print('  - instance-%i)  %s, %s, %s' % (i+1, instance.timestamp, instance.version, os.path.basename(instance.source)))
        #     except IndexError:
        #         print('No instance for ', model.name)
        
        # from ...models import ScientificModel # django database
        # models = ScientificModel.objects.all()
        
        # model = models[344]
        # print(model.name)
        # for i, instance in enumerate(model.instances.all()):
        #     print('  - %i) %s, %s' % (i, instance.version, instance.source))
