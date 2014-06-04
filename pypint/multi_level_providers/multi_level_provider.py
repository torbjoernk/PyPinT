# coding=utf-8
"""
.. moduleauthor:: Torbjörn Klatt <t.klatt@fz-juelich.de>
"""
from collections.abc import Container
from collections.abc import Sized
from collections import OrderedDict
from weakref import ref

from pypint.multi_level_providers.levels.abstract_level import AbstractLevel
from pypint.multi_level_providers.level_transitioners.abstract_level_transitioner import AbstractLevelTransitioner
from pypint.utilities import assert_condition, assert_is_in, assert_is_instance, class_name


class MultiLevelProvider(Container, Sized):
    """Container and Provider of Levels and Transitions between them

    As it is a container (cf. :py:class:`collections.abc.Container`) a given :py:class:`.AbstractLevel` can be tested
    on membership.

    As it is sized (cf. :py:class:`collections.abc.Sized`) the length of it is defined by the number of contained
    levels.
    """

    def __init__(self, *args, **kwargs):
        """
        Parameters
        ----------
        num_levels : :py:class:`int`
            Number of initial levels.
        """
        self._levels = []
        self._level_transitioners = {}

    def level(self, level):
        """Accessor for a level specified by an index.

        Parameters
        ----------
        level : :py:class:`int`
            Level to retrieve integrator for.

        Returns
        -------
        integrator : :py:class:`.AbstractLevel`
            Stored level.
        """
        return self._levels[level]

    def prolongate(self, coarse_data, coarse_level, fine_level=None):
        """Prolongates given data from coarser to finer level.

        Parameters
        ----------
        coarse_data : :py:class:`numpy.ndarray`
            Coarse data to prolongate.

        coarse_level : :py:class:`int`
            Level of the given data to prolongate from.

        fine_level : :py:class:`int`
            *(optional)*
            Fine level to prolongate onto.
            In case it is :py:class:`None` the next finer level is taken.

        Returns
        -------
        prolongated data : :py:class:`numpy.ndarray`
            The prolongated data.

        See Also
        --------
        :py:meth:`.AbstractLevelTransitioner.prolongate` : for details on prolongation
        """
        return self._level_transition(coarse_level=coarse_level, fine_level=fine_level).prolongate(coarse_data)

    def restrict(self, fine_data, fine_level, coarse_level=None):
        """Restringates given data from finer to coarser level.

        Parameters
        ----------
        fine_data :
            Fine data to restrict.

        fine_level : :py:class:`.AbstractLevel`
            Level of the given data to restrict from.

        coarse_level : :py:class:`.AbstractLevel`
            *(optional)*
            Coarse level to restrict onto.
            In case it is :py:class:`None` the next coarser level is taken.

        Returns
        -------
        restringated data : :py:class:`numpy.ndarray`
            The restringated data.

        See Also
        --------
        :py:meth:`.AbstractLevelTransitioner.restrict` : for details on restringation
        """
        return self._level_transition(coarse_level=coarse_level, fine_level=fine_level).restrict(fine_data)

    def add_coarser_level(self, level):
        """Adds a new coarsest level.

        This :py:class:`.MultiLevelProvider` gets cross-referenced to the given level via
        :py:attr:`.AbstractLevel.ml_provider` as a :py:class:`weakref`.

        Parameters
        ----------
        level : :py:class:`.AbstractLevel`

        Raises
        ------
        ValueError
            If ``level`` is not an :py:class:`.AbstractLevel`.
        """
        assert_is_instance(level, AbstractLevel, descriptor="Level", checking_obj=self)
        self._levels.insert(0, level)
        level.ml_provider = ref(self)

    def add_finer_level(self, level):
        """Adds a new finest level.

        This :py:class:`.MultiLevelProvider` gets cross-referenced to the given level via
        :py:attr:`.AbstractLevel.ml_provider` as a :py:class:`weakref`.

        Parameters
        ----------
        level : :py:class:`.AbstractLevel`

        Raises
        ------
        ValueError
            If ``level`` is not an :py:class:`.AbstractLevel`.
        """
        assert_is_instance(level, AbstractLevel, descriptor="Integrator", checking_obj=self)
        self._levels.append(level)
        level.ml_provider = ref(self)

    def add_level_transition(self, transitioner, *args, **kwargs):
        """Adds specialized level transitioner for specified levels.

        Parameters
        ----------
        transitioner : :py:class:`.AbstractLevelTransitioner`
            Special level transitioner for specified prolongation and restringation between given coarse and fine level.

        Raises
        ------
        ValueError
            if ``transitioner`` is not an :py:class:`.AbstractLevelTransitioner`
        """
        assert_is_instance(transitioner, AbstractLevelTransitioner, descriptor="Level Transitioner", checking_obj=self)

        _coarse_level = transitioner.coarse_level
        _fine_level = transitioner.fine_level

        assert_is_in(_coarse_level, self.levels, elem_desc="Coarse Level", list_desc="Levels", checking_obj=self)
        assert_is_in(_fine_level, self.levels, elem_desc="Fine Level", list_desc="Levels", checking_obj=self)

        # extend/initialize level_transition_provider map if necessary
        if _coarse_level not in self._level_transitioners:
            self._level_transitioners[_coarse_level] = {}

        self._level_transitioners[_coarse_level][_fine_level] = transitioner

    def get_coarser_level(self, level):
        assert_is_instance(level, AbstractLevel, descriptor="Level", checking_obj=self)
        assert_condition(level in self,
                         ValueError, message="Given Level is not provided by this MultiLevelProvider",
                         checking_obj=self)
        if level is self.coarsest_level:
            return None
        else:
            return self._levels[self._levels.index(level) - 1]

    def get_finer_level(self, level):
        assert_is_instance(level, AbstractLevel, descriptor="Level", checking_obj=self)
        assert_condition(level in self,
                         ValueError, message="Given Level is not provided by this MultiLevelProvider",
                         checking_obj=self)
        if level is self.finest_level:
            return None
        else:
            return self._levels[self._levels.index(level) + 1]

    @property
    def num_levels(self):
        """Accessor for the number of levels.

        Returns
        -------
        num_levels : :py:class:`int`
            Number of levels of this Multi-Level Provider.
        """
        return len(self._levels)

    @property
    def levels(self):
        return self._levels

    @property
    def coarsest_level(self):
        return self._levels[0]

    @property
    def finest_level(self):
        return self._levels[-1]

    def _level_transition(self, coarse_level=None, fine_level=None):
        """Extracts level transition provider for given coarse and fine levels.

        Parameters
        ----------
        coarse_level : :py:class:`.AbstractLevel`
            Coarse level of the level transitioner.

        fine_level : :py:class:`.AbstractLevel`
            Fine level of the level transitioner.

        Returns
        -------
        level_transitioner : :py:class:`.AbstractLevelTransitioner`
            Level transition provider to restrict and prolongate between the given coarse and fine level.
            In case no specialized transitioner is found, the default one is returned.

        Raises
        ------
        ValueError

            * if ``coarse_level`` and ``fine_level`` are both :py:class:`None`
            * if ``fine_level`` is :py:class:`None` and ``coarse_level`` is the finest one
            * if ``coarse_level`` is :py:class:`None` and ``fine_level`` is the coarsest one
            * if ``fine_level`` or ``coarse_level`` are not in this :py:class:`.MultiLevelProvider`
        """
        assert_condition(coarse_level is not None or fine_level is not None,
                         ValueError, message="Either coarse or fine level index must be given", checking_obj=self)

        if fine_level is None:
            fine_level = self.get_finer_level(coarse_level)
        if coarse_level is None:
            coarse_level = self.get_coarser_level(fine_level)

        assert_condition(fine_level is not None and coarse_level is not None,
                         ValueError,
                         message="Either Fine Level or Coarse Level could not be determined: %s, %s"
                                 % (coarse_level, fine_level),
                         checking_obj=self)
        assert_is_in(coarse_level, self, elem_desc="Coarse Level", list_desc="MultiLevelProvider", checking_obj=self)
        assert_is_in(fine_level, self, elem_desc="Fine Level", list_desc="MultiLevelProvider", checking_obj=self)

        if coarse_level in self._level_transitioners and fine_level in self._level_transitioners[coarse_level]:
            return self._level_transitioners[coarse_level][fine_level]
        else:
            raise RuntimeError("Requested Level Transitioner not available: coarse %s <-> fine %s"
                               % (coarse_level, fine_level))

    def lines_for_log(self):
        _lines = OrderedDict()
        _lines['Number Levels'] = "%d" % self.num_levels
        if self.num_levels > 0:
            _lines['Levels'] = OrderedDict()
            _lines['Levels']['Coarsest'] = self.coarsest_level.lines_for_log()
            if self.num_levels > 1:
                if self.num_levels > 2:
                    for i in range(1, self.num_levels - 1):
                        _lines['Levels']['Intermediate'] = self.levels[i].lines_for_log()
                _lines['Levels']['Finest'] = self.finest_level.lines_for_log()
        else:
            _lines['Levels'] = 'na'

        if len(self._level_transitioners) > 0:
            _lines['Transitioners'] = OrderedDict()
            for _coarse in self._level_transitioners.keys():
                for _fine in self._level_transitioners[_coarse].keys():
                    _lines['Transitioners']["%s <-> %s" % (self.levels.index(_coarse), self.levels.index(_fine))] = \
                        self._level_transition(_coarse, _fine).lines_for_log()
        else:
            _lines['Transitioners'] = 'na'
        return _lines

    def __contains__(self, item):
        if isinstance(item, AbstractLevel):
            return item in self._levels
        else:
            return False

    def __len__(self):
        return self.num_levels

    def __str__(self):
        return "%s<0x%x>(num_level=%d)" % (class_name(self), id(self), self.num_levels)

    def __repr__(self):
        return "<%s at 0x%x : num_level=%d>" % (class_name(self), id(self), self.num_levels)
