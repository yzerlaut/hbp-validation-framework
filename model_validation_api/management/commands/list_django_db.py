from ...models import ScientificModel
import numpy as np
from django.core.management.base import BaseCommand

try:
    raw_input
except NameError:
    raw_input = input
    
data = dict(np.load('/home/yzerlaut/Desktop/Model-Catagol-Spreadsheet.npz'))

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        
        models = ScientificModel.objects.all()

        icount = 0
        for i, model in enumerate(models):
            if len(data['Name'][model.name==data['Name']])>0:
                icount +=1

        print('the spreadsheet containing %i models has %i models from the %i models of the Django database' % (len(data['Name']), icount, len(models)))
