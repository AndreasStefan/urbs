import pyomo.environ
import urbs
import pandas as pd
from pyomo.core import Constraint
from pyomo.opt.base import SolverFactory
import runme
data = urbs.read_excel('Augsburg.xlsx')

data = runme.scenario_base(data)
prob = urbs.create_model(data, timesteps=range(0, 5), dual=True)

optim = SolverFactory('gurobi')
result = optim.solve(prob, tee=True)

res_vertex_duals = urbs.get_entity(prob, 'res_vertex')
marg_costs = pd.DataFrame(res_vertex_duals.xs(('Elec', 'Demand'), level=('com', 'com_type'))).sort_index(axis=0,level='t')

print(marg_costs)
