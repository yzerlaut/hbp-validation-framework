from __future__ import print_function
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets

try:
    from .kg_interaction import check_if_alias_is_already_taken
except ModuleNotFoundError:
    from kg_interaction import check_if_alias_is_already_taken
    

import requests

def check_url_validity(url):
    """ imlemented in the request module """
    return requests.get(url).ok
    
class Registration_Form:
    
    def __init__(self):
        self.Widget_List = {}
        
        self.Widget_List['name'] = interactive(self.f,
                                              x=widgets.Text(\
                                                    value='',
                                                    placeholder='e.g. Layer V Network in CA1',
                                                    description='Name:'));
        self.Widget_List['alias'] = interactive(self.f_alias, {'manual': True, 'manual_name':'Check validity'},
                                              x=widgets.Text(\
                                                    value='',
                                                    placeholder='e.g. L5-CA1_Ntwk',
                                                    description='Alias:'));
        self.Widget_List['contact'] = interactive(self.f,
                                                    x=widgets.Text(\
                                                    value='',
                                                    placeholder='e.g. Smith, John D.',
                                                    description='Contact:'));
        
        self.Widget_List['institution'] = interactive(self.f,
                                                    x=widgets.Text(\
                                                    value='',
                                                    placeholder='e.g. CNRS, France',
                                                    description='Institution:'));
        
        self.Widget_List['contributors'] = interactive(self.f,
                                                    x=widgets.Text(\
                                                    value='',
                                                    description_tooltip='e.g. Smith, John D.; Dupont, Jean Paul; Mueller, Jan; Russo, Giovanni',
                                                    placeholder='e.g. Smith, John D.; Dupont, Jean Paul; Mueller, Jan; Russo, Giovanni',
                                                    description='Contributors:'));
        
        self.Widget_List['description'] = interactive(self.f,
                                                        x=widgets.Textarea(
                                                        placeholder='Decribe the model here',
                                                        description='Description:'))
        # optional figure upload
        self.Widget_List['fig_url'] = interactive(self.f_fig,
                                                {'manual': True, 'manual_name':'Upload figure'},
                                                  x=widgets.Text(\
                                                    value='',
                                                    placeholder='github.com/name/repo/fig.png',
                                                    description='Fig. URL:'));
        self.Widget_List['fig_display'] = widgets.Image(format='png',
                                                        width=50)
        
        self.Widget_List['species'] = interactive(self.f,
                                                        x=widgets.Dropdown(
                                                        options=['',
                                                                 'Homo Sapiens',
                                                                 'Rattus Norvegicus',
                                                                 'Mus Musculus'],
                                                        value='',
                                                        description='Species:'))
                                                  
        self.Widget_List['region'] = interactive(self.f,
                                                        x=widgets.Dropdown(
                                                        options=['', 'Cortex',
                                                                 'Hippocampus',
                                                                 'Cerebellum'],
                                                        value='',
                                                        description='Region:'))
        self.Widget_List['cell_type'] = interactive(self.f,
                                                        x=widgets.Dropdown(
                                                        options=['', 
                                                                 'Pyramidal Cell',
                                                                 'Interneuron'],
                                                        value='',
                                                        description='Cell type:'))
 
        self.Widget_List['scope'] = interactive(self.f,
                                                        x=widgets.Dropdown(
                                                        options=['', 
                                                                 'network',
                                                                 'single cell',
                                                                 'subcellular'],
                                                        value='',
                                                        description='Model scope:'))
        self.Widget_List['abstraction'] = interactive(self.f,
                                                        x=widgets.Dropdown(
                                                        options=['', 
                                                                 'biophysical',
                                                                 'population',
                                                                 'functional'],
                                                        value='',
                                                        description='Abstraction level:'))


        self.Widget_List['license'] = interactive(self.f,
                                                    x=widgets.RadioButtons(
                                                    options=['Free', 'OpenSource', 'CreativeCommons'],
                                                    description='License'))
 
        self.Widget_List['version_text'] = interactive(self.f,
                                                    x=widgets.HTML(placeholder='',
                                                                   value="<b>Add a Version </b> (optional)"))
        self.Widget_List['version_name'] = interactive(self.f,
                                              x=widgets.Text(\
                                                    value='',
                                                    placeholder='e.g. v1.0',
                                                    description='Name:'));
        self.Widget_List['data_url'] = interactive(self.f_url,
                                                {'manual': True, 'manual_name':'Check data availability'},
                                                  x=widgets.Text(\
                                                    value='',
                                                    placeholder='github.com/name/repo',
                                                    description='URL location:'));
        self.Widget_List['commit_id'] = interactive(self.f_commit,
                                                {'manual': True, 'manual_name':'Check commit'},
                                                  x=widgets.Text(\
                                                    value='',
                                                    placeholder='',
                                                    description='Commit:'));
        self.Widget_List['version_description'] = interactive(self.f,
                                                        x=widgets.Textarea(
                                                        placeholder='Decribe the version',
                                                        description='Description:'))
 
        
    def f(self, x):
            return x
        
    def f_alias(self, x):
        check_if_alias_is_already_taken(x)
        return x

    def f_url(self, x):
        """
        checking url validity
        based on the implementation of the request module 
        """
        if requests.get(x).ok:
            print('"%s" is a valid url' % x)
        else:
            print('"%s" does not seem to be a valid url, please check it' % x)            
        return x
    
    def f_commit(self, x):

        baseline_url = self.Widget_List['data_url'].children[0].value
        new_url = baseline_url+'/archive/'+str(x)+'.zip'
        r = requests.get(new_url)
        if r.ok:
            print('downloading archive', new_url, '[...]')
            open('archive.zip', 'wb').write(r.content)
            print('done !')
        else:
            print('"%s" is not a valid commit, please modify it' % x)            
        return x

    def f_fig(self, x):
        """
        downloading the image and displaying it in a widget
        """
        r = requests.get(self.Widget_List['fig_url'].children[0].value)
        open('fig.png', 'wb').write(r.content)
        self.Widget_List['fig_display'].value = open("fig.png", "rb").read()
        self.Widget_List['fig_display'].width = 300

        
    def fill_with_dictionary(self, dictionary):
        for key, val in dictionary.items():
            if key in self.Widget_List:
                self.Widget_List[key].children[0].value = val
            else:
                print('key "%s" is not present in the Registration Form' % key)
            
    def show_registration_form(self):
        print('-----------------------------------------------')
        print('--- MODEL REGISTRATION IN HBP MODEL CATALOG ---')
        print('-----------------------------------------------')
        for key, val in self.Widget_List.items():
            display(val)

    def close_widgets(self):
        for key, val in self.Widget_List.items():
            val.close()

    def print_registration_results(self):
        for key, val in self.Widget_List.items():
            try:
                print(val.result)
            except AttributeError:
                pass



