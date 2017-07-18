import displayRestraintsViews
import displayRestraintsControllers

class DisplayRestraints():
    def __init__(self, parent, restraints):
        self.parent = parent
        self.controller = displayRestraintsControllers.DisplayRestraintsController()
        self.controller.set_restraints(restraints)
        self.controller.count_avg_distances()
        self.view = displayRestraintsViews.DisplayRestraintsView(
            self.parent,
            self.controller,
        )
