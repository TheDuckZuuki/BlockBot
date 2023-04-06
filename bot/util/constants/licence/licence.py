import sys
import os
path = os.getcwd()
# setting path
sys.path.append('../bot')

from util.loaders.yml import read_yml

config = read_yml('config/config')

def licence():
    if config['Licence-Key'] == 'secure.not':
        print('')
        print('Licence key verified!')
        print('')
        return True
    else:
        print('')
        print('Incorrect licence key!')
        print('')