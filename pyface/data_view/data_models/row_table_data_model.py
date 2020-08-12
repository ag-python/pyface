# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" A row-oriented data model implementation.

This module provides a concrete implementation of a data model for the
case of row-oriented data.
"""
from traits.api import Any, ComparisonMode, Instance, List, observe

from pyface.data_view.abstract_data_model import (
    AbstractDataModel, DataViewSetError
)
from pyface.data_view.index_manager import IntIndexManager
from pyface.data_view.data_models.data_accessors import AbstractDataAccessor


class RowTableDataModel(AbstractDataModel):
    """ A data model that presents a list of objects as rows.
    """

    #: A sequence of objects to display in columns.
    data = Any()

    #: An object which describes how to map data for the row headers.
    row_header_data = Instance(AbstractDataAccessor)

    #: An object which describes how to map data for each column.
    column_data = List(
        Instance(AbstractDataAccessor),
        comparison_mode=ComparisonMode.identity,
    )

    #: The index manager that helps convert toolkit indices to data view
    #: indices.
    index_manager = Instance(IntIndexManager, args=())

    def get_column_count(self):
        return len(self.column_data)

    def can_have_children(self, row):
        return len(row) == 0

    def get_row_count(self, row):
        if len(row) == 0:
            return len(self.data)
        else:
            return 0

    def get_value(self, row, column):
        if len(column) == 0:
            column_data = self.row_header_data
        else:
            column_data = self.column_data[column[0]]
        if len(row) == 0:
            return column_data.title
        obj = self.data[row[0]]
        return column_data.get_value(obj)

    def can_set_value(self, row, column):
        if len(row) == 0:
            return False
        if len(column) == 0:
            column_data = self.row_header_data
        else:
            column_data = self.column_data[column[0]]
        obj = self.data[row[0]]
        return column_data.can_set_value(obj)

    def set_value(self, row, column, value):
        if len(row) == 0:
            raise DataViewSetError("Can't set column titles.")
        if len(column) == 0:
            column_data = self.row_header_data
        else:
            column_data = self.column_data[column[0]]
        obj = self.data[row[0]]
        column_data.set_value(obj, value)
        self.values_changed = (row, column, row, column)

    def get_value_type(self, row, column):
        if len(column) == 0:
            column_data = self.row_header_data
        else:
            column_data = self.column_data[column[0]]
        if len(row) == 0:
            return column_data.title_type
        return column_data.value_type

    def _data_default(self):
        return []

    @observe('data')
    def _update_data(self, event):
        self.structure_changed = True

    @observe('row_header_data')
    def _update_row_header_data(self, event):
        self.values_changed = ((), (), (), ())

    @observe('row_header_data:updated')
    def _update_row_header_data_event(self, event):
        if event.new[1] == 'value':
            self.values_changed = ((0,), (), (len(self.data) - 1,), ())
        else:
            self.values_changed = ((), (), (), ())

    @observe('column_data.items')
    def _update_all_column_data_items(self, event):
        self.structure_changed = True

    @observe('column_data:items:updated')
    def _update_column_data(self, event):
        index = self.column_data.index(event.new[0])
        if event.new[1] == 'value':
            self.values_changed = (
                (0,), (index,), (len(self.data) - 1,), (index,)
            )
        else:
            self.values_changed = ((), (index,), (), (index,))