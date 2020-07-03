# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Provides an AbstractDataModel ABC for Pyface data models.

This module provides an ABC for all data view data models.  This specifies
the API that the data view widgets expect, and which the underlying
data is adapted to by the concrete implementations.  Data models are intended
to be toolkit-independent, and be able to adapt any approximately tabular or
nested data structure to what the data view system expects.
"""
from abc import abstractmethod

from traits.api import ABCHasStrictTraits, Event, Instance

from .index_manager import AbstractIndexManager


class AbstractDataModel(ABCHasStrictTraits):
    """ Abstract base class for Pyface data models.

    The data model API is intended to provide a common API for heirarchical
    and tabular data.  This class is concerned with the structure, type and
    values provided by the data, but not with how the data is presented.

    Row and column indices are represented by sequences (usually lists) of
    integers, specifying the index at each level of the heirarchy.  The root
    row and column are represented by empty lists.

    Subclasses need to implement the ``get_column_count``,
    ``can_have_children`` and ``get_row_count`` methods to return the number
    of columns in a particular row, as well as the heirarchical structure of
    the rows.  Appropriate observers should be set up on the underlaying data
    so that the ``structure_changed`` event is fired when the values returned
    by these methods would change.

    Subclasses also have to implement the ``get_value`` and ``get_value_type``
    methods.  These expect a row and column index, with root values treated
    specially: the root row corresponds to the values which will be displayed
    in the column headers of the view, and the root column corresponds to the
    values which will be displayed in the row headers of the view.
    The ``get_value`` returns an arbitrary Python object corresponding to the
    cell being viewed, and the ``get_value_type`` should return an instance of
    an ``AbstractValueType`` that adapts the raw value to the data channels
    that the data view expects (eg. text, color, icons, editable value, etc.).
    Implementations should ensure that the ``values_changed`` event fires
    whenever the data, or the way the data is presented, is updated.


    If the data is to be editable then the subclass should override the
    ``set_value`` method.  It should attempt to change the underlying data as a
    side-effect, and return True on success and False on failure (for example,
    setting an invalid value).  If the underlying data structure cannot be
    listened to internally (such as a numpy array or Pandas data frame), this
    method should also fire the values changed event with appropriate values.
    """

    #: The index manager that helps convert toolkit indices to data view
    #: indices.  This should be an IntIndexManager for non-hierarchical data
    #: or a TupleIndexManager for hierarchical data.
    index_manager = Instance(AbstractIndexManager)

    #: Event fired when the structure of the data changes.
    structure_changed = Event()

    #: Event fired when value changes without changes to structure.  This
    #: should be set to a 4-tuple of (start_row_index, start_column_index,
    #: end_row_index, end_column_index) indicated the subset of data which
    #: changed.  These end values are inclusive, unlike standard Python
    #: slicing notation.
    values_changed = Event()

    # Data structure methods

    @abstractmethod
    def get_column_count(self):
        """ How many columns in the data view model.

        Returns
        -------
        column_count : non-negative int
            The number of columns that the data view provides.  This count
            should not include the row header.
        """
        raise NotImplementedError

    @abstractmethod
    def can_have_children(self, row):
        """ Whether or not a row can have child rows.

        The root row should always return True.

        Parameters
        ----------
        row : sequence of int
            The indices of the row as a sequence from root to leaf.

        Returns
        -------
        can_have_children : bool
            Whether or not the row can ever have child rows.
        """
        raise NotImplementedError

    @abstractmethod
    def get_row_count(self, row):
        """ How many child rows the row currently has.

        Parameters
        ----------
        row : sequence of int
            The indices of the row as a sequence from root to leaf.

        Returns
        -------
        row_count : non-negative int
            The number of child rows that the row has.
        """
        raise NotImplementedError

    # Data value methods

    @abstractmethod
    def get_value(self, row, column):
        """ Return the Python value for the row and column.

        The values for column headers are returned by calling this method with
        row equal to [].  The values for row headers are returned by calling
        this method with column equal to [].

        Parameters
        ----------
        row : sequence of int
            The indices of the row as a sequence from root to leaf.
        column : sequence of int
            The indices of the column as a sequence of length 0 or 1.

        Returns
        -------
        value : any
            The value represented by the given row and column.
        """
        raise NotImplementedError

    def can_set_value(self, row, column):
        """ Whether the value in the indicated row and column can be set.

        The default method assumes the data is read-only and always
        returns False.

        Whether or a column header can be set is returned by calling this
        method with row equal to [].  Whether or a row header can be set
        is returned by calling this method with column equal to [].

        Parameters
        ----------
        row : sequence of int
            The indices of the row as a sequence from root to leaf.
        column : sequence of int
            The indices of the column as a sequence of length 0 or 1.

        Returns
        -------
        can_set_value : bool
            Whether or not the value can be set.
        """
        return False

    def set_value(self, row, column, value):
        """ Set the Python value for the row and column.

        The default method assumes the data is read-only and always
        returns False.

        The values for column headers can be set by calling this method with
        row equal to [].  The values for row headers can be set by calling
        this method with column equal to [].

        Parameters
        ----------
        row : sequence of int
            The indices of the row as a sequence from root to leaf.
        column : sequence of int
            The indices of the column as a sequence of length 0 or 1.
        value : any
            The new value for the given row and column.

        Returns
        -------
        success : bool
            Whether or not the value was set successfully.
        """
        return False

    @abstractmethod
    def get_value_type(self, row, column):
        """ Return the value type of the given row and column.

        The value type for column headers are returned by calling this method
        with row equal to [].  The value types for row headers are returned
        by calling this method with column equal to [].

        Parameters
        ----------
        row : sequence of int
            The indices of the row as a sequence from root to leaf.
        column : sequence of int
            The indices of the column as a sequence of length 0 or 1.

        Returns
        -------
        value_type : AbstractValueType or None
            The value type of the given row and column, or None if no value
            should be displayed.
        """
        raise NotImplementedError

    # Convenience iterator methods

    def iter_rows(self, start_row=()):
        """ Iterator that yields rows in preorder.

        Parameters
        ----------
        start_row : row index
            The row to start at.  The iterator will yeild the row and all
            descendant rows.

        Yields
        ------
        row_index
            The current row index.
        """
        start_row = tuple(start_row)
        yield start_row
        if self.can_have_children(start_row):
            for row in range(self.get_row_count(start_row)):
                yield from self.iter_rows(start_row + (row,))

    def iter_items(self, start_row=()):
        """ Iterator that yields rows and columns in preorder.

        This yields pairs of row, column for all rows in preorder
        and and all column indices for all rows, including [].
        Columns are iterated in order.

        Parameters
        ----------
        start_row : row index
            The row to start iteration from.

        Yields
        ------
        row_index, column_index
            The current row and column indices.
        """
        for row in self.iter_rows(start_row):
            yield row, ()
            for column in range(self.get_column_count(row)):
                yield row, (column,)
