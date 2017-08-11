#------------------------------------------------------------------------------
#
#  Copyright (c) 2005, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in enthought/LICENSE.txt and may be redistributed only
#  under the conditions described in the aforementioned license.  The license
#  is also available online at http://www.enthought.com/licenses/BSD.txt
#
#  Thanks for using Enthought open source!
#
#  Author: Enthought, Inc.
#
#------------------------------------------------------------------------------

""" Enthought pyface package component
"""

# Standard library imports.
import os
import tempfile

from cStringIO import StringIO

# Major package imports.
import wx

# Enthought library imports.
from pyface.resource.api import ResourceFactory

from traits.api import Undefined


class PyfaceResourceFactory(ResourceFactory):
    """ The implementation of a shared resource manager. """

    ###########################################################################
    # 'ResourceFactory' toolkit interface.
    ###########################################################################

    def image_from_file(self, filename):
        """ Creates an image from the data in the specified filename. """

        # N.B 'wx.BITMAP_TYPE_ANY' tells wxPython to attempt to autodetect the
        # --- image format.
        return wx.Image(filename, wx.BITMAP_TYPE_ANY)

    def image_from_data(self, data, filename=None):
        """ Creates an image from the specified data. """
        try:
            return wx.Image(StringIO(data))
        except:
            # wx.Image is only in wx 2.8 or later(?)
            if filename is Undefined:
                return None

        handle = None
        if filename is None:
            # If there is currently no way in wx to create an image from data,
            # we have write it out to a temporary file and then read it back in:
            handle, filename = tempfile.mkstemp()

        # Write it out...
        tf = open(filename, 'wb')
        tf.write(data)
        tf.close()

        # ... and read it back in!  Lovely 8^()
        image = wx.Image(filename, wx.BITMAP_TYPE_ANY)

        # Remove the temporary file.
        if handle is not None:
            os.close(handle)
            os.unlink(filename)

        return image

#### EOF ######################################################################
