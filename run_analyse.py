import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import urbs
from urbs.saveload import load
from comp import get_most_recent_entry
from analyse import glob_result_files
from analyse import plot_cap






directory = get_most_recent_entry('result')
file_names, file_type =  glob_result_files(directory)

for file in file_names:

    if file_type == 'h5':
        h5 = load(file)
        xlsx = None
    elif file_type == 'xlsx':
        h5 = None
        xlsx = file
    # Can be modified
    sites = [None]
    to_drop = ['Slack Elec','Slack Waerme','Slack Fernwaerme']
    plot_sto = False
    plot_cpro = True
    xticks = 2

    for sit in sites:
        fig=plot_cap(prob=h5,resultfile=xlsx, sit=sit, to_drop=to_drop, plot_sto=plot_sto, xticks=xticks)

        scenario_names = os.path.basename(file)
        scenario_names = scenario_names.replace('_', ' ',)
        scenario_names = scenario_names.replace('.h5', '')
        scenario_names = scenario_names.replace('.xlsx', '')
        scenario_names = scenario_names.replace('scenario ', '')


        for ext in ['png', 'pdf']:
            fig.savefig('{}\pro_caps_scenario_{}_{}.{}'.format(directory,scenario_names,sit, ext),
                        bbox_inches='tight')

