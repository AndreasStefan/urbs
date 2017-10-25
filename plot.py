import pandas as pd
import pyomo.environ
from pyomo.opt.base import SolverFactory
import urbs
from urbs.input import get_input
from urbs.output import get_constants, get_timeseries
from urbs.saveload import load
from urbs.input import get_input
from urbs.pyomoio import get_entity, get_entities
from urbs.util import is_string

hdf5_file_name = 'result\mimo-example-20171023T1612\scenario_base.h5'

prob = load(hdf5_file_name )




costs = get_entity(prob, 'costs')