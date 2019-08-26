import os
from fairgraph.client import KGClient
from fairgraph.base import as_list
from fairgraph.brainsimulation import ModelProject
import numpy as np

try:
    from jupyter_collab_storage import oauth_token_handler
    token = oauth_token_handler.get_token()
except ModuleNotFoundError:
    try:
        token = os.environ["HBP_token"]
    except KeyError:
        print('Not able to load the HBP token (neither through the jupyter_collab_storage module nor locally)')

    

def check_if_alias_is_already_taken(name):
    
    print('comparing with KG database [...]')
    client = KGClient(token, nexus_endpoint="https://nexus.humanbrainproject.org/v0")
    MODELS = ModelProject.list(client, size=10000)
    NAMES = [project.name for project in MODELS]
    if name in NAMES:
        i0 = int(np.argwhere(np.array(NAMES, dtype=str)==name))
        if type(MODELS[i0].authors) is list:
            author_list = ''
            for nn in list(MODELS[i0].authors):
                author_list+=nn.resolve(client).full_name+'; '
        else:
            author_list = MODELS[i0].authors.resolve(client).full_name
        print('/!\ --> The alias "%s"' % name, 'is redundant with the following entry:')
        print(''' 
- Description:
        %s
- Author(s):
        %s
        ''' % (MODELS[i0].resolve(client).description[:200]+'  [...]  '+\
               MODELS[i0].resolve(client).description[-200:],
               author_list))
    else:
        print('--> The alias "%s"' % name, 'is valid')
    

if __name__=='__main__':
    check_if_alias_is_already_taken('fs_morphologies')
    check_if_alias_is_already_taken('Multi-scale NN for SWA, SO and AW')
