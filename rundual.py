import pyomo.environ
import urbs
from pyomo.core import Constraint
from pyomo.opt.base import SolverFactory
import runme
data = urbs.read_excel('Augsburg.xlsx')

data = urbs.runme.scenario_base(data)
prob = urbs.create_model(data, timesteps=range(0, 100), dual=True)

optim = SolverFactory('gurobi')
result = optim.solve(prob, tee=True)

res_vertex_duals = urbs.get_entity(prob, 'res_vertex')
marg_costs = res_vertex_duals.xs(('Elec', 'Demand'), level=('com', 'com_type'))
print(marg_costs)
