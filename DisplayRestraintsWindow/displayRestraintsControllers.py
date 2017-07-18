import displayRestraintsModels

import os
import re
import chimera
from chimera import runCommand
from PyRy3D_Extension.Paths import Paths

Paths = Paths()

from configurations import *

class DisplayRestraintsController:
    def __init__(self):
        self.init_model()

    def init_model(self):
        self.model = displayRestraintsModels.DisplayRestraintsModel()

    def change_restraint(self, sel_item):
        sel_index = int(sel_item[0]) - 1
        return self.get_restraint_info_by_ind(sel_index)

    def count_avg_distances(self):
        for restraint in self.model.restraints:
            sum_of_distances = 0
            atoms_a = self.select_atoms_from_restraint(restraint.first)
            atoms_b = self.select_atoms_from_restraint(restraint.second)

            if len(atoms_a) > len(atoms_b):
                tmp = atoms_a
                atoms_a = atoms_b
                atoms_b = tmp

            for i in range(0, len(atoms_a), 1):
                sum_of_distances += self.count_dist_between_atoms(atoms_a[i], atoms_b[i])
            
            avg_dist = round(float(sum_of_distances) / len(atoms_a), 2)
            self.model.avg_distances.append(avg_dist)

    def count_dist_between_atoms(self, atom_a, atom_b):
        dist = atom_a.xformCoord().distance(atom_b.xformCoord())
        return dist

    def create_select_command_from_restraint(self, restraint):
        start = str(restraint.res1_num)
        end = str(restraint.res2_num)
        chain = str(restraint.chain_id)
        command = "select :" + start + "-" + end + "." + chain
        return command

    def get_active_restraint(self):
        return self.model.restraints[self.model.active_restraint_ind]

    def get_name(self):
        return str(self.model.name)

    def get_restraint_by_ind(self, ind):
        return self.model.restraints[ind]

    def get_restraint_info_by_ind(self, ind):
        chain_a = self.model.restraints[ind].first.chain_id
        chain_b = self.model.restraints[ind].second.chain_id
        avg_dist = self.model.avg_distances[ind]
        pred_dist = self.model.restraints[ind].restraint.dist
        return chain_a, chain_b, avg_dist, pred_dist

    def get_restraints(self):
        return self.model.restraints

    def get_visualisation_types(self):
        return self.model.visualisation_types

    def get_restraints_list(self):
        index = 1
        restraints_list = []

        for restraint in self.model.restraints:
            res_1_start = str(restraint.first.res1_num)
            res_1_end = str(restraint.first.res2_num)
            res_2_start = str(restraint.second.res1_num)
            res_2_end = str(restraint.second.res2_num)
            ch_1 = restraint.first.chain_id
            ch_2 = restraint.second.chain_id
            disp_res1 = res_1_start + "-" + res_1_end + "(" + ch_1 + ")"
            disp_res2 = res_2_start + "-" + res_2_end + "(" + ch_2 + ")"
            dispname =  str(index) + ". " + disp_res1 + " <=> " + disp_res2
            restraints_list.append(dispname)
            index += 1

        return restraints_list

    def select_atoms_from_restraint(self, restraint):
        command = self.create_select_command_from_restraint(restraint)
        runCommand(command)
        chain_atoms = chimera.selection.currentAtoms()
        chain_atoms.sort()
        return chain_atoms

    def set_active_restraint(self, index):
        ind = int(index[0]) - 1
        self.model.active_restraint_ind = ind

    def set_restraints(self, restraints):
        self.model.restraints = restraints

    def register_controller(self, name):
        if name == VISUALISATION_TYPES[0]:
            return LadderVisualisationController()
        elif name == VISUALISATION_TYPES[1]:
            return SticksVisualisationController()
        else:
            return LadderVisualisationController()


"""

    Visualization type 1

"""

class VisualisationTypeController(object):
    def __init__(self):
        self.init_model()

    def init_model(self):
        self.model = displayRestraintsModels.VisualisationTypeModel()

    def display_atoms_in_residue(self, residues):
        for residue in residues:
            residue.ribbonDisplay = False
            self.show_atoms_in_residue(residue.atoms)
            
    def draw_restraint(self):
        print "Not implemented."

    def get_active_restraint(self):
        return self.model.active_restraint

    def get_allowed_dist(self):
        return self.model.allowed_dist

    def get_color_option(self):
        return self.model.color_option

    def get_drawing_density(self):
        return self.model.drawing_density

    def get_mainchain_atoms(self, residue_atoms):
        MAINCHAIN = re.compile("^(N|CA|C)$", re.I)
        mainchain = []
        for atom in residue_atoms:
            if MAINCHAIN.match(atom.name) != None:
                mainchain.append(atom)
        return mainchain

    def get_predicted_dist(self):
        return self.model.active_restraint.restraint.dist

    def get_restraint_mainchain_atoms(self):
        chain_a, chain_b = self.select_atoms()
        residue_a, residue_b = self.select_residues()
        mainchain_a = self.get_mainchain_atoms(chain_a)
        mainchain_b = self.get_mainchain_atoms(chain_b)
        return mainchain_a, mainchain_b

    def get_restraint_color(self):
        return self.model.restraint_color

    def get_restraint_transparency(self):
        return self.model.restraint_transparency

    def select_atoms(self):
        chain_1_atoms = self.select_atoms_from_restraint(self.get_active_restraint().first)
        chain_2_atoms = self.select_atoms_from_restraint(self.get_active_restraint().second)
        return chain_1_atoms, chain_2_atoms

    def select_residues(self):
        chain_1_residues = self.__select_residues_from_restraint(self.get_active_restraint().first)
        chain_2_residues = self.__select_residues_from_restraint(self.get_active_restraint().second)
        return chain_1_residues, chain_2_residues

    def set_active_restraint(self, restraint):
        self.model.active_restraint = restraint

    def set_allowed_dist_diff(self, value):
        self.model.allowed_dist = float(value)

    def set_color_option(self, value):
        self.model.color_option = value

    def set_drawing_density(self, value):
        self.model.drawing_density = value

    def set_restraint_transparency(self, value):
        self.model.restraint_transparency = float(value)/100

    def show_atoms_in_residue(self, residue_atoms, show_backbone=False):
        MAINCHAIN = re.compile("^(N|CA|C)$", re.I)
        for atom in residue_atoms:
            if show_backbone:
                atom.display = True
            else:
                atom.display = MAINCHAIN.match(atom.name) != None
            atom.drawMode = chimera.Atom.EndCap

    def update_restraint_color(self, color):
        self.model.restraint_color = color

    def validate_allowed_dist_diff(self, value):
        try:
            value_conv = float(value)
            if value_conv <= 0.0 or value_conv > 200:
                raise ValueError
            else:
                self.set_allowed_dist_diff(value_conv)
                return True
        except ValueError:
            return False

# "STATICS"

    def calculate_dist_into_color(self, avg_dist, color):
        allowed_dist = self.get_allowed_dist()
        color = self.translate_dist_diff_into_color(
            self.get_predicted_dist(),
            avg_dist,
            self.get_allowed_dist(),
        )
        return color

    def count_drawing_density_factor(self, num_of_atoms, density):
        print str(density)
        atoms_to_draw = float(num_of_atoms) * density
        drawing_density_factor = float(num_of_atoms) / float(atoms_to_draw)
        return int(round(drawing_density_factor))

    def count_dist_between_atoms(self, atom_a, atom_b):
        dist = atom_a.xformCoord().distance(atom_b.xformCoord())
        return dist

    def __create_select_command_from_restraint(self, restraint):
        start = str(restraint.res1_num)
        end = str(restraint.res2_num)
        chain = str(restraint.chain_id)
        command = "select :" + start + "-" + end + "." + chain
        return command

    def cut_atoms_count_diff(self, atoms_a, atoms_b):
        if len(atoms_a) == len(atoms_b):
            return atoms_a, atoms_b
        elif len(atoms_a) > len(atoms_b):
            atoms_a = self.cut_atoms_by_starting_index(atoms_a, atoms_b)
            return atoms_b, atoms_a
        elif len(atoms_b) > len(atoms_a):
            atoms_b = self.cut_atoms_by_starting_index(atoms_b, atoms_a)
            return atoms_a, atoms_b

    def cut_atoms_by_starting_index(self, atoms_a, atoms_b):
        num_of_atoms_diff = len(atoms_a) - len(atoms_b)
        starting_index = float(num_of_atoms_diff) / 2
        index = int(round(starting_index))
        atoms_a = atoms_a[index:]
        return atoms_a


    def display_atoms_in_residues(self, residues_a, residues_b):
        self.display_atoms_in_residue(residues_a)
        self.display_atoms_in_residue(residues_b)

    def select_atoms_from_restraint(self, restraint):
        command = self.__create_select_command_from_restraint(restraint)
        runCommand(command)
        chain_atoms = chimera.selection.currentAtoms()
        chain_atoms.sort()
        return chain_atoms

    def __select_residues_from_restraint(self, restraint):
        command = self.__create_select_command_from_restraint(restraint)
        runCommand(command)
        chain_residues = chimera.selection.currentResidues()
        chain_residues.sort()
        return chain_residues

    def translate_dist_diff_into_color(self, pred_dist, dist, allow_diff):
        allowed_dist = allow_diff + pred_dist
        diff = max((dist-pred_dist), 0)
        normalized_diff = min(float(diff * 1) / allowed_dist, 1)
        blue = 0.0
        if 0 <= normalized_diff < 0.5:        #first, green stays at 100%, red raises to 100%
            green = 1.0
            red = 2 * normalized_diff
        if 0.5 <= normalized_diff <= 1:       #then red stays at 100%, green decays
            red = 1.0
            green = 1.0 - 2 * (normalized_diff-0.5)
        return [red, green, blue]

    def translate_into_rgb_01(self, rgb):
        red = float(rgb[0]) / 255.0
        green = float(rgb[1]) / 255.0
        blue = float(rgb[2]) / 255.0
        return [red, green, blue]



"""

    LadderVisualisationTypeController

"""

class LadderVisualisationController(VisualisationTypeController):
    def __init__(self):
        self.init_model()

    def init_model(self):
        self.model = displayRestraintsModels.LadderVisualisationModel()
    
    
    # DRAWING METHODS ==============

    def draw_restraint(self):
        mainchain_a, mainchain_b = super(
            LadderVisualisationController,
            self
        ).get_restraint_mainchain_atoms()
        mainchain_a, mainchain_b = super(
            LadderVisualisationController,
            self
        ).cut_atoms_count_diff(mainchain_a, mainchain_b)

        residues_a, residues_b = super(
            LadderVisualisationController,
            self
        ).select_residues()
        super(
            LadderVisualisationController,
            self
        ).display_atoms_in_residues(residues_a, residues_b)

        self.draw_ladder(
            mainchain_a,
            mainchain_b,
            self.get_color_option(),
            self.get_drawing_type(),
            self.get_drawing_density(),
            self.get_restraint_transparency(),
        )

    def draw_ladder(self, atoms_a, atoms_b, color_opt, drawing_opt, density, transparency):
        bildpath = Paths.pluginpath + BILD_PATH +"/restraints_ladder.bild"
        bildfile = open(bildpath, "w")
        color = super(
            LadderVisualisationController,
            self
        ).translate_into_rgb_01(
            self.get_restraint_color()[0]
        )

        drawing_density_factor = super(
            LadderVisualisationController,
            self
        ).count_drawing_density_factor(
            len(atoms_a),
            density,
        )

        if drawing_opt == 1:
            rect_wall_length = drawing_density_factor
        elif drawing_opt == 2:
            rect_wall_length = 1
            drawing_density_factor *= 2

        for i in range(0, len(atoms_a) - drawing_density_factor, drawing_density_factor):
            points = [
                atoms_a[i].coord(),
                atoms_a[i + rect_wall_length].coord(),
                atoms_b[i + rect_wall_length].coord(),
                atoms_b[i].coord(),
            ]
            if color_opt == 1:
                avg_dist = self.count_avg_dist(atoms_a, i, atoms_b)
                color = super(
                    LadderVisualisationController,
                    self
                ).calculate_dist_into_color(
                    avg_dist,
                    color,
                )
            command = self.draw_sheet(
                color,
                points,
                transparency
                )

            print >> bildfile, str(command)

        bildfile.close()
        runCommand("open " + bildpath)

    def count_avg_dist(self, atoms_a, i, atoms_b):
        dist_1 = self.count_dist_between_atoms(atoms_a[i], atoms_b[i])
        dist_2 = self.count_dist_between_atoms(atoms_a[i + 1], atoms_b[i + 1])
        avg_dist = float((dist_1 + dist_2))/2
        return avg_dist

    def draw_sheet(self, rgb, points, transparency):
        command = ".color " + str(
            rgb[0]) + " " + str(
            rgb[1]) + " " + str(
            rgb[2]) + "\n.transparency " + str(
            transparency) + "\n.polygon "

        for point in points:
            command += str(
                point[0]) + " " + str(
                point[1]) + " " + str(
                point[2]) + " "

        return command

# GETTERS & SETTERS

    def get_drawing_type(self):
        return self.model.drawing_type

    def set_drawing_type(self, value):
        self.model.drawing_type = value


# OTHERS

    def change_drawing_type(self, _val):
        self.set_drawing_type(_val)


"""

    Visualization type 2

"""

class SticksVisualisationController(VisualisationTypeController):
    def __init__(self):
        self.init_model()

    def init_model(self):
        self.model = displayRestraintsModels.SticksVisualisationModel()

    # DRAWING METHODS ==============

    def draw_restraint(self):
        mainchain_a, mainchain_b = super(
            SticksVisualisationController,
            self
        ).get_restraint_mainchain_atoms()
        mainchain_a, mainchain_b = super(
            SticksVisualisationController,
            self
        ).cut_atoms_count_diff(mainchain_a, mainchain_b)

        print "A: " + str(len(mainchain_a))
        print "B: " + str(len(mainchain_b))

        residues_a, residues_b = super(
            SticksVisualisationController,
            self
        ).select_residues()
        super(
            SticksVisualisationController,
            self
        ).display_atoms_in_residues(residues_a, residues_b)

        self.draw_sticks(
            mainchain_a,
            mainchain_b,
            self.get_color_option(),
            self.get_drawing_density(),
            self.get_restraint_transparency(),
        )

    def draw_sticks(self, atoms_a, atoms_b, color_opt, density, transparency):
        bildpath = Paths.pluginpath + BILD_PATH + "/restraints_sticks.bild"
        bildfile = open(bildpath, "w")

        color = super(
            SticksVisualisationController,
            self
        ).translate_into_rgb_01(
            self.get_restraint_color()[0]
        )

        drawing_density_factor = super(
            SticksVisualisationController,
            self
        ).count_drawing_density_factor(
            len(atoms_a),
            density,
        )

        print "A: " + str(len(atoms_a))
        print "B: " + str(len(atoms_b))

        for i in range(0, len(atoms_a), drawing_density_factor):
            point_a = atoms_a[i].coord()
            point_b = atoms_b[i].coord()

            if color_opt == 1:
                avg_dist = self.count_dist_between_atoms(atoms_a[i], atoms_b[i])
                color = super(
                    SticksVisualisationController,
                    self
                ).calculate_dist_into_color(
                    avg_dist,
                    color,
                )
            command = self.draw_tube(
                color,
                point_a,
                point_b,
                transparency
            )
            print >> bildfile, str(command)
 
        bildfile.close()
        runCommand("open " + bildpath)

    def draw_tube(self, rgb, point_a, point_b, transparency, size=0.2):
        command = ".color " + str(
            rgb[0]) + " " + str(
            rgb[1]) + " " + str(
            rgb[2]) + "\n.transparency " + str(
            transparency) + "\n.cylinder " + str(
            point_a[0]) + " " + str(
            point_a[1]) + " " + str(
            point_a[2]) + " " + str(
            point_b[0]) + " " + str(
            point_b[1]) + " " + str(
            point_b[2]) + " " + str(
            size)

        return command
