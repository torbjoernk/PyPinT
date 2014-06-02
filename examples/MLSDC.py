# coding: utf-8
from warnings import simplefilter
simplefilter('always')

from pypint.multi_level_providers.multi_time_level_provider import MultiTimeLevelProvider
from pypint.multi_level_providers.level_transition_providers.time_transition_provider import TimeTransitionProvider
from pypint.utilities.quadrature.sdc_quadrature import SdcQuadrature

base_integrator = SdcQuadrature()
base_integrator.init(num_nodes=3)
# print(base_integrator)

intermediate_integrator = SdcQuadrature()
intermediate_integrator.init(num_nodes=5)
# print(intermediate_integrator)

# fine_integrator = SdcQuadrature()
# fine_integrator.init(num_nodes=7)
# print(fine_integrator)

transitioner1 = TimeTransitionProvider(fine_nodes=intermediate_integrator.nodes, coarse_nodes=base_integrator.nodes)
# print(transitioner1)
# transitioner2 = TimeTransitionProvider(fine_nodes=fine_integrator.nodes, coarse_nodes=intermediate_integrator.nodes)
# print(transitioner2)

ml_provider = MultiTimeLevelProvider()
# ml_provider.add_coarse_level(fine_integrator)
ml_provider.add_coarse_level(intermediate_integrator)
ml_provider.add_coarse_level(base_integrator)
ml_provider.add_level_transition(transitioner1, 0, 1)
# ml_provider.add_level_transition(transitioner2, 1, 2)
print(ml_provider)

from examples.problems.lambda_u import LambdaU
# problem = Constant()
problem = LambdaU(lmbda=complex(-1.0, -1.0))
print(problem)


from pypint.communicators import ForwardSendingMessaging
comm = ForwardSendingMessaging()


from pypint.solvers.ml_sdc import MlSdc
mlsdc = MlSdc(communicator=comm)
comm.link_solvers(previous=comm, next=comm)
comm.write_buffer(tag=(ml_provider.num_levels - 1), value=problem.initial_value, time_point=problem.time_start)


mlsdc.init(problem=problem, ml_provider=ml_provider)

from pypint.integrators.sdc import SemiImplicitMlSdc
mlsdc.run(SemiImplicitMlSdc, dt=1.0)

print("RHS Evaluations: %d" % problem.rhs_evaluations)
