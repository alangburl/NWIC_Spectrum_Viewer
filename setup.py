#This is the setup script. It will build the required packages for your
#version of python. If you don't have Cython. It will download it for you
#using pip install cython
import sys
import subprocess
try:
    import cython
except ImportError as e:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install','cython'])
    reqs = subprocess.check_output([sys.executable, '-m', 'pip','freeze'])
    install=[r.decode().split('==')[0] for r in reqs.split()]
    print('Installed: {}'.format(install))

files_to_build=['conversion_setup.py',
                'ROI_Arrival_setup.py',
                'timing_setup.py']

for i in files_to_build:
    subprocess.check_call(['python', i, 'build_ext', '--inplace'])
    