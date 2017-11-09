import matplotlib as mpl
import matplotlib.pyplot as plt
import os
from urbs.urbs.saveload import load

from urbs.analyse import plot_cap
from urbs.analyse import glob_result_files
from urbs.analyse import get_most_recent_entry




directory = get_most_recent_entry('result')
hdf5_file_names =  glob_result_files(directory)

for hdf5_file_name in hdf5_file_names:

    prob = load(hdf5_file_name)

    sit = 'Augsburg'
    to_drop = []
    plot_sto = True
    plot_cpro = True
    xticks = 2

    fig=plot_cap(prob=prob, sit=sit, to_drop=to_drop, plot_sto=plot_sto, xticks=xticks)

    scenario_names = [os.path.basename(rf)  # drop folder names, keep filename
                          .replace('_', ' ')  # replace _ with spaces
                          .replace('.h5', '')  # drop file extension
                          .replace('scenario ', '')  # drop 'scenario ' prefix
                      for rf in hdf5_file_name]

    for ext in ['png', 'pdf']:
        fig.savefig('{}\scenario_base_{}.{}'.format(directory,sit, ext),
                    bbox_inches='tight')

