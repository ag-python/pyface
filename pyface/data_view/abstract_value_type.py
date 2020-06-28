# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Provides an AbstractValueType ABC for Pyface data models.

This module provides an ABC for data view value types, which are responsible
for adapting raw data values as used by the data model's ``get_value`` and
``set_value`` methods to the data channels that the data view expects, such
as text, color, icons, etc.

It is up to the data view to take this standardized data and determine what
and how to actually display it.
"""

from traits.api import ABCHasStrictTraits, Event, observe


class AbstractValueType(ABCHasStrictTraits):
    """ A value type converts raw data into data channels.

    The data channels are editor value, text, color, image, and description.
    The data channels are used by other parts of the code to produce the actual
    display.

    Subclasses should mark traits that potentially affect the display of values
    with ``update=True`` metdadata, or alternatively fire the ``updated``
    event when the state of the value type changes.
    """

    #: Fired when a change occurs that requires updating values.
    updated = Event

    def can_edit(self, model, row, column):
        """ Return whether or not the value can be edited.

        The default implementation is that cells that can be set are
        editable.

        Parameters
        ----------
        model : AbstractDataModel
            The data model holding the data.
        row : sequence of int
            The row in the data model being queried.
        column : sequence of int
            The column in the data model being queried.

        Returns
        -------
        can_edit : bool
            Whether or not the value is editable.
        """
        return model.can_set_value(row, column)

    def get_editable(self, model, row, column):
        """ Return a value suitable for editing.

        The default implementation is to return the underlying data value
        directly from the data model.

        Parameters
        ----------
        model : AbstractDataModel
            The data model holding the data.
        row : sequence of int
            The row in the data model being queried.
        column : sequence of int
            The column in the data model being queried.

        Returns
        -------
        value : any
            The value to edit.
        """
        return model.get_value(row, column)

    def set_editable(self, model, row, column, value):
        """ Set a value that is returned from editing.

        The default implementation is to set the value directly from the
        data model.  Returns True if successful, False if it fails.

        Parameters
        ----------
        model : AbstractDataModel
            The data model holding the data.
        row : sequence of int
            The row in the data model being queried.
        column : sequence of int
            The column in the data model being queried.
        value : any
            The value to set.

        Returns
        -------
        success : bool
            Whether or not the value was successfully set.
        """
        if not self.can_edit(model, row, column):
            return False
        return model.set_value(row, column, value)

    def has_text(self, model, row, column):
        """ Whether or not the value has a textual representation.

        The default implementation returns True if ``get_text``
        returns a non-empty value.

        Parameters
        ----------
        model : AbstractDataModel
            The data model holding the data.
        row : sequence of int
            The row in the data model being queried.
        column : sequence of int
            The column in the data model being queried.

        Returns
        -------
        has_text : bool
            Whether or not the value has a textual representation.
        """
        return self.get_text(model, row, column) != ""

    def get_text(self, model, row, column):
        """ The textual representation of the underlying value.

        The default implementation calls str() on the underlying value.

        Parameters
        ----------
        model : AbstractDataModel
            The data model holding the data.
        row : sequence of int
            The row in the data model being queried.
        column : sequence of int
            The column in the data model being queried.

        Returns
        -------
        text : str
            The value to edit.
        """
        return str(model.get_value(row, column))

    def set_text(self, model, row, column, text):
        """ Set the text of the underlying value.

        This is provided primarily for backends which may not permit
        non-text editing of values, in which case this provides an
        alternative route to setting the value.  The default implementation
        does not allow setting the text.

        Parameters
        ----------
        model : AbstractDataModel
            The data model holding the data.
        row : sequence of int
            The row in the data model being queried.
        column : sequence of int
            The column in the data model being queried.
        text : str
            The text to set.

        Returns
        -------
        success : bool
            Whether or not the value was successfully set.
        """
        return False

    @observe('+update')
    def update_value_type(self, event=None):
        """ Fire update event when marked traits change. """
        self.updated = True