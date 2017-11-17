import os
import urbs
from urbs.input import get_input
from urbs.output import get_constants, get_timeseries
import glob
import math
import matplotlib.gridspec as gridspec
import matplotlib.ticker as tkr
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import pandas as pd
from urbs.input import split_columns

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

font = {'family' : 'sans-serif',
        'weight' : 'bold',
        'size'   : 22}

mpl.rc('font', **font)

def plot_cap(prob=None, resultfile=None, sit=None, fontsize=16, show=True, to_drop=None, plot_sto=True, plot_cpro=True,
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
def get_data(resultfile):

    #read excel resultfile
    resultfile = resultfile
    xls = pd.ExcelFile(resultfile)  # read resultfile
    com_sums = xls.parse('Commodity sums', index_col=[0, 1])
    com_sums.columns = split_columns(com_sums.columns, '.')

    #define colors
    cmap = plt.cm.gist_ncar
    colors_all = cmap(np.linspace(0., 2.5, len(com_sums)))

    #get all sites and demands
    sites = list(com_sums.columns.levels[0])
    demands = list(com_sums.columns.levels[1])

    #define all dicts
    com_sums_loc = {}
    color_dict_consume = {}
    color_dict_export = {}
    color_dict_produce = {}
    color_dict_import = {}
    drop_zeros = []
    timeseries_dict = {}

    produced_per_month = {}
    consumed_per_month = {}
    export_per_month = {}
    import_per_month = {}
    produced_per_week = {}
    consumed_per_week = {}
    export_per_week = {}
    import_per_week = {}

    #timesteps per month
    jan = np.arange(1, 24 * 31 + 1, 1)
    feb = np.arange(jan[-1] + 1, (24 * 28 + 1) + jan[-1], 1)
    mar = np.arange(feb[-1] + 1, (24 * 31 + 1) + feb[-1], 1)
    apr = np.arange(mar[-1] + 1, (24 * 30 + 1) + mar[-1], 1)
    mai = np.arange(apr[-1] + 1, (24 * 31 + 1) + apr[-1], 1)
    jun = np.arange(mai[-1] + 1, (24 * 30 + 1) + mai[-1], 1)
    jul = np.arange(jun[-1] + 1, (24 * 31 + 1) + jun[-1], 1)
    aug = np.arange(jul[-1] + 1, (24 * 31 + 1) + jul[-1], 1)
    sep = np.arange(aug[-1] + 1, (24 * 30 + 1) + aug[-1], 1)
    okt = np.arange(sep[-1] + 1, (24 * 31 + 1) + sep[-1], 1)
    nov = np.arange(okt[-1] + 1, (24 * 30 + 1) + okt[-1], 1)
    dez = np.arange(nov[-1] + 1, (24 * 31 + 1) + nov[-1], 1)

    # timesteps per week
    x1 = np.arange(1, 8737, 1)  # year has 52,14 weeks
    x1 = np.split(x1, 52)

    #read timeseries dat from excel sheet and prepare for plot
    for sit in sites:
        for demand in demands:
            produced_per_month1 = pd.DataFrame()
            consumed_per_month1 = pd.DataFrame()
            export_per_month1 = pd.DataFrame()
            import_per_month1 = pd.DataFrame()
            produced_per_week1 = pd.DataFrame()
            consumed_per_week1 = pd.DataFrame()
            export_per_week1 = pd.DataFrame()
            import_per_week1 = pd.DataFrame()
            temp = []
            color_dict_consume.update({(sit, demand): np.argwhere(com_sums.loc['Consumed', (sit, demand,)] > 1e-4)})
            color_dict_produce.update({(sit, demand): np.argwhere(com_sums.loc['Created', (sit, demand,)] > 1e-4)})
            timeseries_name = ('{}.{} timeseries'.format(sit, demand))
            timeseries_name = timeseries_name[:31]
            temp = pd.DataFrame(xls.parse(timeseries_name, header=[0, 1], index_col=[0]))
            timeseries_dict.update({(sit, demand): temp})

            for j, time in enumerate([jan, feb, mar, apr, mai, jun, jul, aug, sep, okt, nov, dez]):
                temp_sum = []
                temp_sum = temp.loc[time, 'Created'].sum()
                produced_per_month1 = pd.concat(
                    [produced_per_month1, pd.DataFrame(temp_sum.values, index=temp_sum.index,
                                                       columns=[[sit], [demand], [j]])], axis=1)

                temp_sum = []
                temp_sum = temp.loc[time, 'Consumed'].sum()
                consumed_per_month1 = pd.concat(
                    [consumed_per_month1, pd.DataFrame(temp_sum.values, index=temp_sum.index,
                                                       columns=[[sit], [demand], [j]])], axis=1)

                try:
                    temp_sum = []
                    temp_sum = temp.loc[time, 'Import from'].sum()
                    import_per_month1 = pd.concat(
                        [import_per_month1, pd.DataFrame(temp_sum.values, index=temp_sum.index,
                                                         columns=[[sit], [demand], [j]])], axis=1)

                except:
                    pass

                try:
                    temp_sum = []
                    temp_sum = temp.loc[time, 'Export to'].sum()
                    export_per_month1 = pd.concat(
                        [export_per_month1, pd.DataFrame(temp_sum.values, index=temp_sum.index,
                                                         columns=[[sit], [demand], [j]])], axis=1)


                except:
                    pass
            produced_per_month.update({(sit, demand): pd.DataFrame(produced_per_month1)})
            consumed_per_month.update({(sit, demand): pd.DataFrame(consumed_per_month1)})
            export_per_month.update({(sit, demand): pd.DataFrame(export_per_month1)})
            import_per_month.update({(sit, demand): pd.DataFrame(import_per_month1)})

            for j, i in enumerate(np.arange(1, 53, 1)):
                temp_sum = []
                temp_sum = temp.loc[x1[j:j + 1][0], 'Created'].sum()
                produced_per_week1 = pd.concat([produced_per_week1, pd.DataFrame(temp_sum.values, index=temp_sum.index,
                                                                                 columns=[[sit], [demand], [j]])],
                                               axis=1)

                temp_sum = []
                temp_sum = temp.loc[x1[j:j + 1][0], 'Consumed'].sum()
                consumed_per_week1 = pd.concat([consumed_per_week1, pd.DataFrame(temp_sum.values, index=temp_sum.index,
                                                                                 columns=[[sit], [demand], [j]])],
                                               axis=1)

                try:
                    temp_sum = []
                    temp_sum = temp.loc[x1[j:j + 1][0], 'Import from'].sum()
                    import_per_week1 = pd.concat([import_per_week1, pd.DataFrame(temp_sum.values, index=temp_sum.index,
                                                                                 columns=[[sit], [demand], [j]])],
                                                 axis=1)

                except:
                    pass

                try:
                    temp_sum = []
                    temp_sum = temp.loc[x1[j:j + 1][0], 'Export to'].sum()
                    export_per_week1 = pd.concat([export_per_week1, pd.DataFrame(temp_sum.values, index=temp_sum.index,
                                                                                 columns=[[sit], [demand], [j]])],
                                                 axis=1)

                except:
                    pass
            produced_per_week.update({(sit, demand): pd.DataFrame(produced_per_week1)})
            consumed_per_week.update({(sit, demand): pd.DataFrame(consumed_per_week1)})
            export_per_week.update({(sit, demand): pd.DataFrame(export_per_week1)})
            import_per_week.update({(sit, demand): pd.DataFrame(import_per_week1)})

            try:
                color_dict_export.update({(sit, demand): np.argwhere(com_sums.loc['Export', (sit, demand,)] > 1e-4)})
            except:
                pass
            try:
                color_dict_import.update({(sit, demand): np.argwhere(com_sums.loc['Import', (sit, demand,)] > 1e-4)})
            except:
                pass

            drop_zeros = com_sums.loc[:, (sit, demand)]
            drop_zeros = drop_zeros[drop_zeros > 1e-4]
            com_sums_loc.update({(sit, demand): drop_zeros})

    return colors_all,sites,demands,color_dict_produce,color_dict_consume,color_dict_export,color_dict_import,produced_per_week,consumed_per_week,export_per_week,import_per_week,produced_per_month,consumed_per_month,export_per_month,import_per_month,com_sums_loc






def energy_year(resultfile,typ='consumed'):
    colors_all,sites, demands,color_dict_produce, color_dict_consume, color_dict_export, color_dict_import, produced_per_week, consumed_per_week, export_per_week, import_per_week, produced_per_month, consumed_per_month, export_per_month, import_per_month, com_sums_loc =get_data(resultfile=resultfile)

    for sit in sites:
        for demand in demands:
            if typ == 'consumed':
                dat = pd.DataFrame(com_sums_loc[sit, demand].loc['Consumed'])
                color_dict = color_dict_consume
                try:
                    dat = dat.append(pd.DataFrame(com_sums_loc[sit, demand].loc['Export']))
                    color_dict_extra = color_dict_export
                except:
                    pass
            else:
                dat = pd.DataFrame(com_sums_loc[sit, demand].loc['Created'])
                color_dict = color_dict_produce
                try:
                    dat = dat.append(pd.DataFrame(com_sums_loc[sit, demand].loc['Import']))
                    color_dict_extra = color_dict_import
                except:
                    pass

            color_array = colors_all[color_dict[sit, demand]]
            try:
                color_array_extra = colors_all[color_dict_extra[sit, demand]]
            except:
                pass
            try:
                color_array = color_array.reshape((color_array.shape[0], -1))
            except:
                pass
            try:
                color_array_extra = color_array_extra.reshape((color_array_extra.shape[0], -1))
            except:
                pass
            try:
                color_array = np.concatenate((color_array, color_array_extra))
            except:
                pass


            fig1, ax1 = plt.subplots()
            labels = dat.index
            plt.pie(dat, explode=None, colors=color_array, labels=None, autopct=my_autopct, shadow=False,
                    pctdistance=0.8, startangle=90)
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            ax1.legend(labels, loc='upper center', bbox_to_anchor=(1.01, 0.9))
            plt.title(('{} {}').format(sit, demand))
            plt.show()
    return
def energy_month(resultfile,typ='consumed'):
    colors_all, sites, demands, color_dict_produce, color_dict_consume, color_dict_export, color_dict_import, produced_per_week, consumed_per_week, export_per_week, import_per_week, produced_per_month, consumed_per_month, export_per_month, import_per_month, com_sums_loc = get_data(
        resultfile=resultfile)

    for sit in sites:
        for demand in demands:
            if demand == 'CO2' and typ =='consumed':
                pass
            else:
                fig = plt.figure(figsize=(20, 8))
                ax = plt.subplot()
                if typ == 'consumed':
                    try:
                        frames = [
                            pd.DataFrame(consumed_per_month[sit, demand][(consumed_per_month[sit, demand].T > 1e-4).any()]),
                            pd.DataFrame(export_per_month[sit, demand][(export_per_month[sit, demand].T > 1e-4).any()])]

                        to_plot = pd.concat(frames)
                        color_array = colors_all[color_dict_consume[sit, demand]]
                        color_array_extra = colors_all[color_dict_export[sit, demand]]
                        color_array = np.concatenate((color_array, color_array_extra))

                    except:
                        to_plot = pd.DataFrame(
                            consumed_per_month[sit, demand][(consumed_per_month[sit, demand].T > 1e-4).any()])
                        color_array = colors_all[color_dict_produce[sit, demand]]

                    try:
                        color_array = color_array.reshape((color_array.shape[0], -1))
                    except:
                        pass
                else:
                    try:
                        frames = [pd.DataFrame(
                            produced_per_month[sit, demand][(produced_per_month[sit, demand].T > 1e-4).any()]),
                                  pd.DataFrame(
                                      import_per_month[sit, demand][(import_per_month[sit, demand].T > 1e-4).any()])]

                        to_plot = pd.concat(frames)
                        color_array = colors_all[color_dict_produce[sit, demand]]
                        color_array_extra = colors_all[color_dict_import[sit, demand]]
                        color_array = np.concatenate((color_array, color_array_extra))

                    except:
                        to_plot = pd.DataFrame(
                            produced_per_month[sit, demand][(produced_per_month[sit, demand].T > 1e-4).any()])
                        color_array = colors_all[color_dict_produce[sit, demand]]

                    try:
                        color_array = color_array.reshape((color_array.shape[0], -1))
                    except:
                        pass


                labels = to_plot.index
                bottom = np.zeros(len(to_plot[sit, demand].columns))
                ind = np.arange(len(to_plot[sit, demand].columns))
                width = 0.5
                for elem, color in zip((to_plot.values), color_array):
                    plt.bar(ind, elem / 1e3, width, bottom=bottom, color=color)
                    bottom += elem / 1e3

                ax.xaxis.grid(False)
                ax.yaxis.grid(True, 'major', linestyle='-')

                ax.yaxis.set_ticks_position('none')

                # group 1,000,000 with commas
                group_thousands = tkr.FuncFormatter(lambda x,
                                                           pos: '{:0,d}'.format(int(x)))
                ax.yaxis.set_major_formatter(group_thousands)
                if demand == 'CO2':
                    ax.set_ylabel('kt')
                else:
                    ax.set_ylabel('GWh')

                ax.legend(labels, loc='upper center', bbox_to_anchor=(1.2, 0.9))
                plt.xticks(ind, ('jan', 'feb', 'mar', 'apr', 'mai', 'jun', 'jul', 'aug', 'sep', 'okt', 'nov', 'dez'))
                plt.title('{} {} {}'.format(sit, demand,typ))
                fig.tight_layout()
                plt.show()





    return fig
def glob_result_files(folder_name):
    """ Glob hdf5 files from specified folder.

    Args:
        folder_name: an absolute or relative path to a directory

    Returns:
        list of filenames that match the pattern 'scenario_*.h5'
    """


    glob_pattern = os.path.join(folder_name, 'scenario_*.h5')
    result_files = sorted(glob.glob(glob_pattern))

    if len(result_files) == 0:
        file_type = 'xlsx'
        glob_pattern = os.path.join(folder_name, 'scenario_*.xlsx')
        result_files = sorted(glob.glob(glob_pattern))
    else:
        file_type = 'h5'

    return result_files, file_type


def my_autopct(pct):
    return ('%.0f' % pct) if pct > 10 else ''



