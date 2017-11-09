import os
import urbs
from urbs.urbs.input import get_input
from urbs.urbs.output import get_constants, get_timeseries
from urbs.urbs.input import get_input
from urbs.urbs.pyomoio import get_entity, get_entities
from urbs.urbs.util import is_string
from urbs.urbs.saveload import load
import glob
import math
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import os
import pandas as pd
import sys

COLOURS = {
    0: 'lightsteelblue',
    1: 'cornflowerblue',
    2: 'royalblue',
    3: 'lightgreen',
    4: 'salmon',
    5: 'mediumseagreen',
    6: 'orchid',
    7: 'burlywood',
    8: 'palegoldenrod',
    9: 'sage',
    10: 'lightskyblue',
    11: 'firebrick',
    12: 'blue',
    13: 'darkgreen'}


def plot_cap(prob=None, resultfile=None, sit=None, fontsize=16, show=True, to_drop=[], plot_sto=True, plot_cpro=True,
             xticks=None):
    """Process and storage capacities
    Creates a horizontal barplot of the new and installed capacities of processes and storages
    Args:
    prob: a ficus model instance
    resultfile: a stored ficus resultfile
    fontsize: fontsize for labels/legend in figure
    to_drop: Processes which should be dropped
    plot_sto: if False storage caps will not be shown
    plot_sto: if False process caps will not be shown
    xticks: define xticks


    Returns:
    fig: figure handle

    Example:
    import urbs
    from urbs.input import get_input
    from urbs.output import get_constants, get_timeseries
    from urbs.saveload import load
    from urbs.input import get_input
    from urbs.pyomoio import get_entity, get_entities
    from urbs.util import is_string


    hdf5_file_name = 'result\P2X-20171103T0813\scenario_base.h5'
    prob = load(hdf5_file_name)
    plot_cap(prob,sit='Bayern',to_drop=['Slack H2', 'Slack powerplant', 'Slack traffic'],plot_sto=False, xticks=3)


    """
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    import numpy as np
    plt.ion()

    ##Get Data and Prepare Data##
    ##############

    # Read either form given instance or saved resultfile
    if (prob is None) and (resultfile is None):
        # either prob or resultfile must be given
        raise NotImplementedError('please specify either "prob" or "resultfile"!')
    elif (prob is not None) and (resultfile is not None):
        # either prob or resultfile must be given
        raise NotImplementedError('please specify EITHER "prob" or "resultfile"!')
    elif resultfile is None:
        # prob is given, get timeseries from prob
        costs, cpro, ctra, csto = get_constants(prob)
    else:
        # resultfile is given, get timeseries from resultfile
        xls = pd.ExcelFile(resultfile)  # read resultfile
        cpro = xls.parse('Process caps', index_col=[0, 1])
        csto = xls.parse('Storage caps', index_col=[0, 1, 2])

    if sit is None:
        # delete index with zero capacity and delete defined processes for all sits
        try:
            csto = csto.groupby(level=['sto']).sum()

            csto = csto[csto['C Total'] > 1e-1]
        except ValueError:
            pass
        try:
            cpro = cpro.groupby(level=['Process']).sum()

            cpro = cpro.drop(to_drop)

            cpro = cpro[cpro['Total'] > 1e-1]
        except ValueError:
            pass

    else:
        # delete index with zero capacity and delete defined processes of defined sit
        try:
            csto = csto.loc[sit]
            csto = csto.groupby(level=['sto']).sum()
            csto = csto[csto['C Total'] > 1e-1]
        except ValueError:
            pass
        try:
            cpro = cpro.loc[sit]
            cpro = cpro.drop(to_drop)
            cpro = cpro[cpro['Total'] > 1e-1]
        except ValueError:
            pass

    # define xticks
    if xticks is None:
        xticks = 2

    ##PLOT##
    ##############
    # FIGURE
    fig = plt.figure(figsize=(11, 7))

    if csto.empty and cpro.empty:
        # No Processes and storages
        return fig
    elif csto.empty:
        gs = mpl.gridspec.GridSpec(1, 1)
    elif cpro.empty:
        gs = mpl.gridspec.GridSpec(1, 2)
    else:
        height_ratio = [cpro.index.size, csto.index.size]
        gs = mpl.gridspec.GridSpec(2, 2, height_ratios=height_ratio)
    axes = []

    if cpro.empty or plot_cpro is False:
        ofs = 2  # offset for storage plot axes index
        sharex = None
    else:
        # PLOT PROCESS
        ofs = 0
        ax0 = plt.subplot(gs[0])
        yticks = np.arange(len(cpro))
        ax0.barh(yticks, cpro['Total'] - cpro['New'], color=COLOURS[1], align='center')
        ax0.barh(yticks, cpro['New'], \
                 left=cpro['Total'] - cpro['New'], color=COLOURS[3], align='center')
        ax0.set_yticks(yticks)
        ax0.set_yticklabels(cpro.index)
        axes.append(ax0)
        sharex = ax0

    if csto.empty or plot_sto is False:
        # If no storage exists, only show process capacities
        ax0.set_xlabel('Power Capacity (MW)', fontsize=fontsize)
        ax0.set_xticks(ax0.get_xticks()[::xticks])
        ax0.set_xlim(0, ax0.get_xlim()[1] * 1.1)
        loc = 'upper right'
    else:
        # PLOT STORAGE
        # Plot Power Capacities
        ax2 = plt.subplot(gs[2 - ofs], sharex=sharex)
        yticks = np.arange(len(csto))
        ax2.barh(yticks, csto['P Total'] - csto['P New'], color=COLOURS[1], align='center')
        ax2.barh(yticks, csto['P New'], \
                 left=csto['P Total'] - csto['P New'], color=COLOURS[3], align='center')
        ax2.set_yticks(yticks)
        ax2.set_yticklabels(csto.index)
        ax2.set_xlabel('Power Capacity (MW)', fontsize=fontsize)
        ax2.set_xticks(ax2.get_xticks()[::xticks])
        ax2.set_xlim(0, ax2.get_xlim()[1] * 1.1)
        axes.append(ax2)

        # Plot Energy Capacities
        ax3 = plt.subplot(gs[3 - ofs])
        ax3.barh(yticks, csto['C Total'] - csto['C New'], color=COLOURS[1], align='center')
        ax3.barh(yticks, csto['C New'], \
                 left=csto['C Total'] - csto['C New'], color=COLOURS[3], align='center')
        ax3.set_yticks(yticks)
        ax3.set_yticklabels([], visible=False)
        ax3.set_xlabel('Energy Capacity (MWh)', fontsize=fontsize)
        ax3.set_xticks(ax3.get_xticks()[::xticks])
        ax3.set_xlim(0, ax3.get_xlim()[1] * 1.1)
        axes.append(ax3)
        loc = 'upper center'
        if not cpro.empty:
            plt.setp(ax0.get_xticklabels(), visible=False)
            loc = 'upper left'

    ##AXES Properties##
    ##############
    for ax in axes:
        ax.grid()
        ax.set_ylim(ax.get_yticks()[0] - 0.5, ax.get_yticks()[-1] + 0.5)
        ax.tick_params(labelsize=fontsize - 2)
        # group 1,000,000 with commas
        group_thousands = mpl.ticker.FuncFormatter(
            lambda x, pos: '{:0,d}'.format(int(x)))
        ax.xaxis.set_major_formatter(group_thousands)

    ##LEGEND##
    ##############
    if not cpro.empty:
        ax0.plot([], [], color=COLOURS[1], linestyle='None', marker='s', label='Installed', markersize=12)
        ax0.plot([], [], color=COLOURS[3], linestyle='None', marker='s', label='New', markersize=12)
        lg = ax0.legend(frameon=False,
                        ncol=1,
                        loc=loc,
                        bbox_to_anchor=(1.0, 0.5),
                        borderaxespad=0.,
                        fontsize=fontsize - 2,
                        numpoints=1)
    else:
        ax2.plot([], [], color=COLOURS[1], linestyle='None', marker='s', label='Installed', markersize=12)
        ax2.plot([], [], color=COLOURS[3], linestyle='None', marker='s', label='New', markersize=12)
        lg = ax2.legend(frameon=False,
                        ncol=2,
                        loc=loc,
                        bbox_to_anchor=(1.0, 0.5),
                        borderaxespad=0.,
                        fontsize=fontsize - 2,
                        numpoints=1)

    fig.tight_layout()
    if show is True:
        try:

            plt.show(block=False)
        except TypeError:
            plt.show()

    return fig


def get_most_recent_entry(search_dir):
    """ Return most recently modified entry from given directory.

    Args:
        search_dir: an absolute or relative path to a directory

    Returns:
        The file/folder in search_dir that has the most recent 'modified'
        datetime.
    """
    entries = glob.glob(os.path.join(search_dir, "*"))
    entries.sort(key=lambda x: os.path.getmtime(x))
    return entries[-1]


def glob_result_files(folder_name):
    """ Glob hdf5 files from specified folder.

    Args:
        folder_name: an absolute or relative path to a directory

    Returns:
        list of filenames that match the pattern 'scenario_*.h5'
    """


    glob_pattern = os.path.join(folder_name, 'scenario_*.h5')
    result_files = sorted(glob.glob(glob_pattern))
    return result_files


def compare_scenarios(result_files, output_filename):
    """ Create report sheet and plots for given report spreadsheets.

    Args:
        result_files: a list of spreadsheet filenames generated by urbs.report
        output_filename: a spreadsheet filename that the comparison is to be
                         written to

     Returns:
        Nothing

    To do:
        Don't use report spreadsheets, instead load pickled problem
        instances. This would make this function less fragile and dependent
        on the output format of urbs.report().
    """

    # derive list of scenario names for column labels/figure captions
    scenario_names = [os.path.basename(rf)  # drop folder names, keep filename
                      .replace('_', ' ')  # replace _ with spaces
                      .replace('.h5', '')  # drop file extension
                      .replace('scenario ', '')  # drop 'scenario ' prefix
                      for rf in result_files]

    # find base scenario and put at first position
    try:
        base_scenario = scenario_names.index('base')
        result_files.append(result_files.pop(base_scenario))
        scenario_names.append(scenario_names.pop(base_scenario))
    except ValueError:
        pass  # do nothing if no base scenario is found

    prob = {}

    # READ

    for rf in result_files:
        with load(rf) as instance:
            prob[rf]=instance



