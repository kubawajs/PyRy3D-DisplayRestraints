from configurations import *

class DisplayRestraintsModel:
    def __init__(self):
        self.name = WINDOW_NAME
        self.restraints = []
        self.avg_distances = []
        self.visualisation_types = VISUALISATION_TYPES
        self.active_restraint_ind = 0

class VisualisationTypeModel(object):
    def __init__(self):
        self.name = "Not assigned"
        self.active_restraint = None
        self.allowed_dist = DEFAULT_ALLOWED_DIFF
        self.color_option = 1
        self.drawing_density = 1.0
        self.restraint_color = DEFAULT_COLOR
        self.restraint_transparency = DEFAULT_TRANSPARENCY

class LadderVisualisationModel(VisualisationTypeModel):
    def __init__(self):
        super(LadderVisualisationModel, self).__init__()
        self.name = VISUALISATION_TYPES[0]
        self.drawing_type = 1

class SticksVisualisationModel(VisualisationTypeModel):
    def __init__(self):
        super(SticksVisualisationModel, self).__init__()
        self.name = VISUALISATION_TYPES[1]