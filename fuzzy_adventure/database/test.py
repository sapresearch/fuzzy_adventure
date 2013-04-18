import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'

import sys
sys.path.append('/home/I834397/Git/fuzzy_adventure/database/')

from transactions.models import Transactions
trans = Transactions.objects.all()

print trans[0].start_date