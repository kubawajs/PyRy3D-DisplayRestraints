import chimera.extension

class DisplayRestraintsEMO(chimera.extension.EMO):

    def name(self):
        return 'Display Restraints'

    def description(self):
        return 'Tool for visualizing restraints in macromolecular complexes.'

    def categories(self):
        return ['Utilities']

    def icon(self):
        return None

    def activate(self):
        dialog = self.module('gui').DisplayRestraintsDialog
        from chimera import dialogs
        dialogs.display(dialog.name)
        return None


chimera.extension.manager.registerExtension(DisplayRestraintsEMO(__file__))
