import os

import chimera
from chimera.baseDialog import ModelessDialog


class DisplayRestraintsDialog(ModelessDialog):

    # Properties
    name = "Display Restraints"
    buttons = ("Close")
    help = ("https://github.com/kubawajs/PyRy3D-DisplayRestraints", DisplayRestraintsApp)
    title = "Display Restraints"


# Register app
chimera.dialogs.register(DisplayRestraintsDialog.name, DisplayRestraintsDialog)

dir, file = os.path.split(__file__)
icon = os.path.join(dir, 'ExtensionUI.tiff')
chimera.tkgui.app.toolbar.add(icon, lambda d=chimera.dialogs.display,
                              n=DisplayRestraintsDialog.name: d(n), 'Display Restraints', None)
