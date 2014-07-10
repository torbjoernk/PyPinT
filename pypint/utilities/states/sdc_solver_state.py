# coding=utf-8
"""
.. moduleauthor:: Torbjörn Klatt <t.klatt@fz-juelich.de>
"""
from pypint.utilities.states.solver_state import SolverState
from pypint.utilities.states.iteration_state import IterationState
from pypint.utilities.states.timestep_state import TimeStepState
from pypint.utilities.states.node_state import NodeState
from pypint.solutions.final_solution import FinalSolution
from pypint.solutions.iterative_solution import IterativeSolution
from pypint.solutions.data_storage.trajectory_solution_data import TrajectorySolutionData
from pypint.utilities.assertions import assert_named_argument


class SdcSolverState(SolverState):
    def __init__(self, **kwargs):
        kwargs['element_type'] = [IterationState, TimeStepState, NodeState]
        kwargs['solution_type'] = [FinalSolution, IterativeSolution, TrajectorySolutionData]

        assert_named_argument('num_nodes', kwargs, types=int, descriptor='Number of Nodes per Time Step')
        kwargs['num_states'] = [0, kwargs.get('num_time_steps', 1), kwargs['num_nodes']]
        if 'num_time_steps' in kwargs:
            del kwargs['num_time_steps']
        del kwargs['num_nodes']
        super(SolverState, self).__init__(**kwargs)


__all__ = ['SdcSolverState']
