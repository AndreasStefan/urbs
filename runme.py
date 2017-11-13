import os
import pandas as pd
import math
import pyomo.environ
import shutil
import urbs
from datetime import datetime
from pyomo.opt.base import SolverFactory


# SCENARIOS
def scenario_base(data):

    return data


def scenario_stock_prices(data):
    # change stock commodity prices
    co = data['commodity']
    stock_commodities_only = (co.index.get_level_values('Type') == 'Stock')
    co.loc[stock_commodities_only, 'price'] *= 1.5
    return data


def scenario_co2_limit(data):
    # change global CO2 limit
    global_prop = data['global_prop']
    global_prop.loc['CO2 limit', 'value'] *= 0.05
    return data


def scenario_co2_tax_mid(data):
    # change CO2 price in Mid
    co = data['commodity']
    co.loc[('Mid', 'CO2', 'Env'), 'price'] = 50
    return data


def scenario_north_process_caps(data):
    # change maximum installable capacity
    pro = data['process']
    pro.loc[('North', 'Hydro plant'), 'cap-up'] *= 0.5
    pro.loc[('North', 'Biomass plant'), 'cap-up'] *= 0.25
    return data


def scenario_no_dsm(data):
    # empty the DSM dataframe completely
    data['dsm'] = pd.DataFrame()
    return data


def scenario_all_together(data):
    # combine all other scenarios
    data = scenario_stock_prices(data)
    data = scenario_co2_limit(data)
    data = scenario_north_process_caps(data)
    return data


def prepare_result_directory(result_name):
    """ create a time stamped directory within the result folder """
    # timestamp for result directory
    now = datetime.now().strftime('%Y%m%dT%H%M')

    # create result directory if not existent
    result_dir = os.path.join('result', '{}-{}'.format(result_name, now))
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    return result_dir


def setup_solver(optim, logfile='solver.log'):
    """ """
    if optim.name == 'gurobi':
        # reference with list of option names
        # http://www.gurobi.com/documentation/5.6/reference-manual/parameters
        optim.set_options("logfile={}".format(logfile))
        optim.set_options("timelimit=7200")  # seconds
        optim.set_options("mipgap=10e-4")  # default = 1e-4
    elif optim.name == 'glpk':
        # reference with list of options
        # execute 'glpsol --help'
        optim.set_options("log={}".format(logfile))
        # optim.set_options("tmlim=7200")  # seconds
        # optim.set_options("mipgap=.0005")
    else:
        print("Warning from setup_solver: no options set for solver "
              "'{}'!".format(optim.name))
    return optim


def run_scenario(input_file, timesteps, scenario, result_dir,
                 plot_tuples=None, plot_periods=None, report_tuples=None):
    """ run an urbs model for given input, time steps and scenario

    Args:
        input_file: filename to an Excel spreadsheet for urbs.read_excel
        timesteps: a list of timesteps, e.g. range(0,8761)
        scenario: a scenario function that modifies the input data dict
        result_dir: directory name for result spreadsheet and plots
        plot_tuples: (optional) list of plot tuples (c.f. urbs.result_figures)
        plot_periods: (optional) dict of plot periods (c.f. urbs.result_figures)
        report_tuples: (optional) list of (sit, com) tuples (c.f. urbs.report)

    Returns:
        the urbs model instance
    """

    # scenario name, read and modify data for scenario
    sce = scenario.__name__
    data = urbs.read_excel(input_file)
    data = scenario(data)

    # create model
    prob = urbs.create_model(data, timesteps)

    # refresh time stamp string and create filename for logfile
    now = prob.created
    log_filename = os.path.join(result_dir, '{}.log').format(sce)

    # solve model and read results
    optim = SolverFactory('gurobi')  # cplex, glpk, gurobi, ...
    optim = setup_solver(optim, logfile=log_filename)
    result = optim.solve(prob, tee=True)

    # save problem solution (and input data) to HDF5 file
    urbs.save(prob, os.path.join(result_dir, '{}.h5'.format(sce)))

    # write report to spreadsheet
    urbs.report(
        prob,
        os.path.join(result_dir, '{}.xlsx').format(sce),
        report_tuples=report_tuples)

    # result plots
    urbs.result_figures(
        prob,
        os.path.join(result_dir, '{}'.format(sce)),
        plot_title_prefix=sce.replace('_', ' '),
        plot_tuples=plot_tuples,
        periods=plot_periods,
        figure_size=(24, 9))
    return prob



def Wind(year):

    inv_costs = (6.089e+11)*math.exp((year*(-0.006443)))
    fix_costs = inv_costs*(2/100)

    return inv_costs,fix_costs


def PV_Freiflaeche(year):
    inv_costs = ( 3.185e+24) * math.exp((year * (-0.021)))
    fix_costs = inv_costs * (1.5 / 100)

    return inv_costs, fix_costs

def PV_Dach(year):
    inv_costs = (4.432e+15) * math.exp((year * (-0.01092)))
    fix_costs = inv_costs * (2 / 100)

    return inv_costs, fix_costs

def Laufwasser(year):
    inv_costs = (2.17e+06) * math.exp((year * (0.0004661)))
    fix_costs = inv_costs * (4.5 / 100)

    return inv_costs, fix_costs

def Gasturbine(year):
    inv_costs = (9.088e+06) * math.exp((year * (-0.001092)))
    fix_costs = inv_costs * (5.2 / 100)

    return inv_costs, fix_costs

def GuD(year):
    inv_costs = (2.03e+06 ) * math.exp((year * (0)))
    fix_costs = inv_costs * (5.2 / 100)

    return inv_costs, fix_costs

def Heizwerk(year):

    inv_costs = (153400/0.94) * (year **(0))
    fix_costs = inv_costs * (2 / 100)

    return inv_costs, fix_costs

def Biogas_KWK(year):
    inv_costs = (1.358e+19) * math.exp((year * (-0.01437)))
    fix_costs = inv_costs * (6.1 / 100)

    return inv_costs, fix_costs


def Biogas_Aufbereitung(year):
    inv_costs = (1.458e+14) * math.exp((year * (-0.009123)))
    fix_costs = inv_costs * (6 / 100)

    return inv_costs, fix_costs

def Abfall_KWK(year):
    inv_costs = (3.993e+13) * math.exp((year * (-0.007803)))
    fix_costs = inv_costs * (4.5/ 100)

    return inv_costs, fix_costs

def Solar_dez(year):
    inv_costs = (300000) * math.exp((year * (0)))
    fix_costs = inv_costs * (1.3/ 100)

    return inv_costs, fix_costs

def Solar_zentr(year):
    inv_costs = (190000) * math.exp((year * (0)))
    fix_costs = inv_costs * (1.4/ 100)

    return inv_costs, fix_costs

def Biomasse_KWK(year):
    inv_costs = (4.911e+15) * math.exp((year * (-0.01056)))
    fix_costs = inv_costs * (3.3/ 100)

    return inv_costs, fix_costs

def Oelkessel(year):

    inv_costs = (863000) * (year **(0))
    fix_costs = inv_costs * (1/ 100)

    return inv_costs, fix_costs

def Holzkessel(year):
    inv_costs = (2.528e+11) * math.exp((year *(-0.006021)))
    fix_costs = inv_costs * (2/ 100)

    return inv_costs, fix_costs

def Gaskessel(year):

    inv_costs = (660000) * (year **(0))
    fix_costs = inv_costs * (1/ 100)

    return inv_costs, fix_costs

def GWWP(year):
    inv_costs = (1.218e+11) * math.exp((year * (-0.005767)))
    fix_costs = inv_costs * (4/ 100)

    return inv_costs, fix_costs

def Batterie(year):

    inv_costs_p = (3.47e+55) * math.exp((year * (-0.05709)))
    fix_costs_p = inv_costs_p * (1.4/ 100)
    inv_costs_e = (1.357e+49) * math.exp((year * (-0.04957)))


    return inv_costs_p, fix_costs_p,inv_costs_e


def Waermenetz(year):

    inv_costs_p = (1.044e+09) * math.exp((year * (-0.00354)))
    fix_costs_p = inv_costs_p * (3/ 100)

    return inv_costs_p, fix_costs_p


def Puffer_zentr(year):

    inv_costs_p = (200000) * (year **(0))
    fix_costs_p = inv_costs_p * (1/ 100)
    inv_costs_e = (3869) * (year **(0))


    return inv_costs_p, fix_costs_p,inv_costs_e

def Puffer_dez(year):

    inv_costs_p = (150000) * (year **(0))
    fix_costs_p = inv_costs_p * (1/ 100)
    inv_costs_e = (42992) * (year **(0))


    return inv_costs_p, fix_costs_p,inv_costs_e

if __name__ == '__main__':
    input_file = 'Augsburg.xlsx'
    result_name = os.path.splitext(input_file)[0]  # cut away file extension
    result_dir = prepare_result_directory(result_name)  # name + time stamp
    runme = 'runme.py'

    # copy input file to result directory
    shutil.copyfile(input_file, os.path.join(result_dir, input_file))
    # copy runme.py to result directory
    shutil.copyfile(runme, os.path.join(result_dir, runme))

    # simulation timesteps
    (offset, length) = (1, 20)  # time step selection
    timesteps = range(offset, offset+length+1)

    # plotting commodities/sites
    plot_tuples = [
        ('Augsburg', 'Elec'),
        ('Augsburg', 'Nahwaerme'),
        ('Augsburg', 'Waerme dezentral'),
        ('Augsburg', 'HG W_PV'),
        ('Augsburg', 'HG W_Solar'),
        ('Augsburg', 'HG W_GWWP'),
        ('Augsburg', 'HG S_PV'),
        ('Augsburg', 'HG P2H_SP')
        ]

    # detailed reporting commodity/sites
    report_tuples = [
        ('Augsburg', 'Elec'), ('Augsburg', 'Nahwaerme'), ('Augsburg', 'Waerme dezentral'),
        ('Augsburg', 'CO2'), ('Augsburg', 'HG W_PV'),('Augsburg', 'HG W_GWWP'),('Augsburg', 'HG W_Solar'),('Augsburg', 'HG S_PV'),('Augsburg', 'HG P2H_SP')]

    # plotting timesteps
    plot_periods = {
        'all': timesteps[1:]
    }

    # add or change plot colors
    my_colors = {
        'Augsburg': (230, 200, 200),
        }
    for country, color in my_colors.items():
        urbs.COLORS[country] = color

    # select scenarios to be run
    scenarios = [
        scenario_base]
        #scenario_stock_prices,
        #scenario_co2_limit,
        #scenario_co2_tax_mid,
        #scenario_no_dsm,
        #scenario_north_process_caps,
        #scenario_all_together]

    for scenario in scenarios:
        prob = run_scenario(input_file, timesteps, scenario, result_dir,
                            plot_tuples=plot_tuples,
                            plot_periods=plot_periods,
                            report_tuples=report_tuples)

