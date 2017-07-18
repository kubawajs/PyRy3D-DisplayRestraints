try:
    import Tkinter
except:
    import tkinter as Tkinter

import tkMessageBox
import tkColorChooser
import Pmw
import displayRestraintsControllers

from configurations import *

""" 

    Main window class view
    
"""

class DisplayRestraintsView:
    def __init__(self, parent, controller):
        self.controller = controller
        self.parent = parent
        self.create_view()

    def create_view(self):
        self.create_display_window()
        self.create_restraints_info_frame()
        self.create_tabs()
        self.create_bottom_buttons()

# DISPLAY WINDOW ============================

    def create_display_window(self):
        self.display_window = Tkinter.Toplevel(master=self.parent)
        self.display_window.title(self.controller.get_name())
        self.display_window.config(
            padx=WINDOW_PADX,
            pady=WINDOW_PADY,
        )
        
# TABS ======================================

    def create_tabs(self):
        self.visualisation_types = self.controller.get_visualisation_types()
        self.create_notebook(self.display_window)

    def create_notebook(self, parent):
        self.notebook = Pmw.NoteBook(parent)
        self.notebook.pack(
            fill="both",
            expand=1,
            padx=0,
            pady=LABEL_PADY,
        )
        self.visualisation_methods = []
        for name in VISUALISATION_TYPES:
            self.create_tab(name, self.notebook)

    def create_tab(self, tab_name, _notebook):
        tab = _notebook.add(tab_name)
        sub_controller = self.controller.register_controller(tab_name)
        self.partial_view = self.return_view(
            tab,
            sub_controller,
            tab_name,
        )
        self.partial_view.controller.set_active_restraint(
            self.controller.get_active_restraint()
        )
        self.visualisation_methods.append(self.partial_view)

# BOTTOM BUTTONS ============================

    def create_bottom_buttons(self):
        self.bottom_buttons_label = Tkinter.Label(
            self.display_window,
        )
        self.create_draw_button(self.bottom_buttons_label)
        self.create_close_button(self.bottom_buttons_label)
        self.bottom_buttons_label.pack(padx=LABEL_PADX, pady=LABEL_PADY)

    def create_draw_button(self, parent):
        self.button_draw = Tkinter.Button(
            parent,
            text=BUTTON_DRAW_TEXT,
            padx=BUTTON_PADX,
            pady=BUTTON_PADY,
            command=self.draw_restraint,
        )
        self.button_draw.grid(
            row=0,
            column=0,
        )

    def create_close_button(self, parent):
        self.button_draw = Tkinter.Button(
            parent,
            text=BUTTON_CLOSE_TEXT,
            padx=BUTTON_PADX,
            pady=BUTTON_PADY,
            command=self.close_window,
        )
        self.button_draw.grid(
            row=0,
            column=1,
        )

    def draw_restraint(self):
        cur_sel = self.notebook.getcurselection()
        cur_ind = self.notebook.index(cur_sel)
        self.visualisation_methods[cur_ind].controller.draw_restraint()

# RESTRAINTS INFO FRAME =====================

    def create_restraints_info_frame(self):
        self.create_restraints_label_frame(self.display_window)
        
        parent = self.restraints_label_frame
        self.create_restraints_label(parent)
        self.create_restraints_combobox(parent)
        self.create_restraint_info_label(parent)

    def create_restraints_label_frame(self, parent):
        self.restraints_label_frame = Tkinter.LabelFrame(
            parent,
            text=RESTRAINTS_LABEL_FRAME_TEXT,
            padx=LABEL_PADX,
            pady=LABEL_PADY,
        )
        self.restraints_label_frame.pack(
            fill="x",
        )
    
    def create_restraints_label(self, parent):
        self.restraints_label = Tkinter.Label(
            parent,
            text=RESTRAINTS_LABEL_TEXT,
            padx=LABEL_PADX,
            pady=LABEL_PADY,
        )
        self.restraints_label.pack()
    
    def create_restraints_combobox(self, parent):
        restraints_list = self.controller.get_restraints_list()

        self.restraints_combobox = Pmw.ComboBox(
            parent,
            scrolledlist_items=restraints_list,
            listheight=COMBOBOX_HEIGHT,
            entryfield_entry_state="readonly",
            selectioncommand=self.change_restraint,
        )
        if len(restraints_list) != 0:
            self.restraints_combobox.setvalue(restraints_list[0])
        self.restraints_combobox.pack(
            fill="x",
            padx=LABEL_PADX,
            pady=LABEL_PADY
        )

    def create_restraint_info_label(self, parent):
        self.create_restraint_data_frame(parent)
        self.config_data_frame_grid()
        self.restraint_data_frame.pack()

    def config_data_frame_grid(self):
        self.restraint_data_frame.grid_columnconfigure(0, weight=1)
        self.restraint_data_frame.grid_columnconfigure(1, weight=1)

    def create_restraint_data_frame(self, parent):
        self.restraint_data_frame = Tkinter.LabelFrame(
            parent,
            text=RESTRAINT_DATA_FRAME_TEXT,
            padx=LABEL_PADX,
            pady=LABEL_PADY,
        )
        self.add_restraint_data_frame_labels(self.restraint_data_frame)
        self.add_restraint_data_frame_values(self.restraint_data_frame)
        self.restraint_data_frame.pack(fill="both", padx=LABEL_PADX, pady=LABEL_PADY)
    
    def add_restraint_data_frame_labels(self, parent):
        self.restraint_data_frame_tmp = Tkinter.Frame(
            parent,
            padx=LABEL_PADX,
            pady=LABEL_PADY,
        )
        self.setup_restraint_labels(self.restraint_data_frame)
        self.restraint_data_frame_tmp.grid(
            row=0,
            column=0,
            sticky="W",
        )

    def add_restraint_data_frame_values(self, parent):
        self.restraint_data_frame_tmp = Tkinter.Frame(
            parent,
            padx=LABEL_PADX,
            pady=LABEL_PADY,
        )
        self.setup_restraint_values(self.restraint_data_frame)
        self.restraint_data_frame_tmp.grid(
            row=0,
            column=1,
            sticky="W",
        )
    
    def setup_restraint_labels(self, parent):
        self.restraint_labels = []
        self.pred_dist_label = self.add_restraint_data_frame_label(parent, PREDICTED_DISTANCE_TEXT, 0, 0)
        self.avg_dist_label = self.add_restraint_data_frame_label(parent, AVERAGE_DISTANCE_TEXT, 1, 0)
        self.chain_a_label = self.add_restraint_data_frame_label(parent, CHAIN_A_TEXT, 2, 0)
        self.chain_b_label = self.add_restraint_data_frame_label(parent, CHAIN_B_TEXT, 3, 0)
        
    def setup_restraint_values(self, parent):
        self.add_restraint_data_frame_label(parent, NOT_SELECTED_TEXT, 2, 1)
        self.add_restraint_data_frame_label(parent, NOT_SELECTED_TEXT, 3, 1)
        self.add_restraint_data_frame_label(parent, NO_DISTANCE_TEXT, 0, 1)
        self.add_restraint_data_frame_label(parent, NO_DISTANCE_TEXT, 1, 1)
        
    def add_restraint_data_frame_label(self, parent, text, row_num, col_num):
        self.label = Tkinter.Label(
            parent,
            text=text
        )
        self.label.grid(
            row=row_num,
            column=col_num,
            sticky="W",
        )
        self.restraint_labels.append(self.label)

    def change_restraint(self, _sel_item):
        chain_a, chain_b, avg_dist, pred_dist = self.controller.change_restraint(
            _sel_item
            )
        self.controller.set_active_restraint(_sel_item)
        self.edit_restraints_info_frame_values(chain_a, chain_b, avg_dist, pred_dist)
        active = self.controller.get_active_restraint()
        for vis in self.visualisation_methods:
            vis.controller.set_active_restraint(
                active,
            )

    def edit_restraints_info_frame_values(self, chain_a, chain_b, avg_dist, pred_dist):
        self.restraint_labels[4].configure(
            text=str(chain_a)
        )
        self.restraint_labels[5].configure(
            text=str(chain_b)
        )
        self.restraint_labels[6].configure(
            text=str(pred_dist)
        )
        self.restraint_labels[7].configure(
            text=str(avg_dist)
        )

# EVENTS ====================================

    def close_window(self):
        self.display_window.destroy()

# REGISTER TYPE =============================

    def return_view(self, parent, controller, name):
        if name == VISUALISATION_TYPES[0]:
            return LadderVisualisationView(parent, controller)
        elif name == VISUALISATION_TYPES[1]:
            return SticksVisualisationView(parent, controller)
        else:
            return LadderVisualisationView(parent, controller)

"""
    
    Visualisation type class view
    
"""

class VisualisationTypeView(object):
    def __init__(self, parent, controller):
        self.controller = controller
        self.parent = parent
        self.create_view()

    def create_view(self):
        self.create_display_options_label_frame(self.parent)
        self.create_transparency_options(self.display_option_label_frame)
        self.create_color_options(self.display_option_label_frame)
        self.create_drawing_density(self.display_option_label_frame)

# DISPLAY OPTION LABEL FRAME ===============

    def create_display_options_label_frame(self, parent):
        self.display_option_label_frame = Tkinter.LabelFrame(
            parent,
            text=DISPLAY_OPTIONS_TEXT,
            padx=LABEL_PADX,
            pady=LABEL_PADY,
        )
        self.display_option_label_frame.pack(
            fill="x",
            padx=LABEL_PADX,
            pady=LABEL_PADY,
        )

# TRANSPARENCY OPTIONS =======================

    def create_transparency_options(self, parent):
        self.create_transparency_frame(parent)
        self.create_transparency_slider(self.transparency_frame)

    def create_transparency_frame(self, parent):
        self.transparency_frame = Tkinter.LabelFrame(
            parent,
            text=TRANSPARENCY_FRAME_TEXT,
            padx=LABEL_PADX,
            pady=LABEL_PADY,
        )
        self.transparency_frame.pack(
            fill="x",
        )

    def create_transparency_slider(self, parent):
        self.transparency_slider = Tkinter.Scale(
            parent,
            from_=0,
            to=100,
            command = self.set_restraint_transparency,
            orient="horizontal",
        )
        self.transparency_slider.set(DEFAULT_TRANSPARENCY*100)
        self.transparency_slider.pack(
            fill="x",
        )

    def set_restraint_transparency(self, value):
        self.controller.set_restraint_transparency(value)

# COLOR OPTIONS ============================

    def create_color_options(self, parent):
        self.create_color_options_frame(parent)
        self.create_color_radiobuttons(self.color_options_frame)
        self.create_color_chooser(self.color_options_frame)
        self.create_dist_diff_options(self.color_options_frame)

    def create_dist_diff_options(self, parent):
        self.create_allowed_dist_diff_change_label(parent)
        self.create_dist_diff_set_opt(parent)

    def create_color_options_frame(self, parent):
        self.color_options_frame = Tkinter.LabelFrame(
            parent,
            text=COLOR_OPTIONS_TEXT,
            padx=LABEL_PADX,
            pady=LABEL_PADY,
        )
        self.config_color_options_frame_grid()
        self.color_options_frame.pack(
            fill="x",
        )
        
    def config_color_options_frame_grid(self):
        self.color_options_frame.grid_columnconfigure(
            0,
            weight=2,
        )
        self.color_options_frame.grid_columnconfigure(
            1,
            weight=1,
        )

    # LEFT FRAME
        
    def create_color_radiobuttons(self, parent):
        self.color_radiobuttons = Tkinter.Frame(
            parent,
        )
        self.config_color_options_radiobuttons(self.color_radiobuttons)
        self.color_radiobuttons.grid(
            row=0,
            column=0,
            sticky="w",
        )

    def config_color_options_radiobuttons(self, parent):
        self.color_option_value = Tkinter.IntVar(parent)
        self.color_option_value.set(1)
        for text, val in COLORING_OPTIONS:
            Tkinter.Radiobutton(
                parent,
                text=text,
                variable=self.color_option_value,
                command=self.activate_color_chooser,
                value=val,
            ).pack(
                anchor="w",
            )

    def activate_color_chooser(self):
        color = self.controller.get_restraint_color()[1]
        if self.color_option_value.get() == 2:
            self.color_chooser_button.configure(
                state="active",
                activebackground=color,
            )
        else:
            self.color_chooser_button.configure(
                state="disabled",
                bg=DISABLED_BUTTON_COLOR[1],
            )
        self.controller.set_color_option(self.color_option_value.get())

    def create_allowed_dist_diff_change_label(self, parent):
        value = str(self.controller.get_allowed_dist())
        self.allowed_dist_diff_label = Tkinter.Label(
            parent,
            text=ALLOWED_DIST_DIFF_TEXT + " " + value,
        )
        self.allowed_dist_diff_label.grid(
            row=2,
            column=0,
        )

    def update_allowed_dist_diff_change_label(self):
        value = str(self.controller.get_allowed_dist())
        self.allowed_dist_diff_label.configure(
            text=ALLOWED_DIST_DIFF_TEXT + " " + value,
        )
    
    # RIGHT FRAME

    def create_color_chooser(self, parent):
        self.color_chooser_frame = Tkinter.Frame(
            parent,
        )
        self.create_color_chooser_button_label(self.color_chooser_frame)
        self.create_color_chooser_button(self.color_chooser_frame)
        self.color_chooser_frame.grid(
            row=0,
            column=1,
        )
    
    def create_color_chooser_button_label(self, parent):
        self.color_chooser_button_label = Tkinter.Label(
            parent,
            text=COLOR_CHOOSER_BUTTON_LABEL_TEXT,
        )
        self.color_chooser_button_label.pack()

    def create_color_chooser_button(self, parent):
        color = self.controller.get_restraint_color()[1]
        self.color_chooser_button = Tkinter.Button(
            parent,
            command= lambda: self.show_color_window(
                parent,
            ),
            bg=DISABLED_BUTTON_COLOR[1],
            state="disabled",
        )
        self.color_chooser_button.pack(
            fill="x",
            padx=LABEL_PADX,
        )

    def show_color_window(self, parent):
        color = self.controller.get_restraint_color()[1]
        _color = tkColorChooser.askcolor(
            color=color,
            parent=parent,
            title=COLOR_WINDOW_TEXT,
        )
        self.update_color_button_color(_color)
        self.controller.update_restraint_color(_color)

    def update_color_button_color(self, color):
        self.color_chooser_button.configure(
            bg=color[1],
        )

    def create_allowed_dist_diff_textbox(self, parent):
        self.content = Tkinter.FloatType()
        self.allowed_dist_diff_textbox = Tkinter.Entry(
            parent,
            textvariable=self.content,
            width=5,
        )
        self.allowed_dist_diff_textbox.grid(
            row=0,
            column=0,
        )

    def create_set_allowed_dist_diff_button(self, parent):
        self.set_allowed_dist_diff_button = Tkinter.Button(
            parent,
            text="Set",
            padx=5,
            pady=0,
            command=self.set_allowed_dist_diff,
        )
        self.set_allowed_dist_diff_button.grid(
            row=0,
            column=1,
        )
    
    def set_allowed_dist_diff(self):
        set_dist = self.allowed_dist_diff_textbox.get()
        if self.controller.validate_allowed_dist_diff(set_dist):
            self.update_allowed_dist_diff_change_label()
        else:
            self.show_error_dialog_box()

    def create_dist_diff_set_opt(self, parent):
        self.create_dist_diff_set_frame(parent)
        self.create_allowed_dist_diff_textbox(self.dist_diff_set_frame)
        self.create_set_allowed_dist_diff_button(self.dist_diff_set_frame)

    def create_dist_diff_set_frame(self, parent):
        self.dist_diff_set_frame = Tkinter.Frame(
            parent,
        )
        self.dist_diff_set_frame.grid(
            row=2,
            column=1,
        )

    def show_error_dialog_box(self):
        tkMessageBox.showerror(
            "Wrong value",
            "Wrong value. Enter a numeric value greater than 0 and lower than 200.",
            parent=self.parent,
        )

# DRAWING DENSITY ============================

    def create_drawing_density(self, parent):
        self.create_drawing_density_frame(parent)
        self.create_drawing_density_label(self.drawing_density_frame)
        self.create_drawing_density_combobox(self.drawing_density_frame)

    def create_drawing_density_frame(self, parent):
        self.drawing_density_frame = Tkinter.Frame(
            parent,
            padx=LABEL_PADX,
            pady=LABEL_PADY,
        )
        self.config_drawing_density_frame_grid()
        self.drawing_density_frame.pack(
            fill="x",
        )
        
    def config_drawing_density_frame_grid(self):
        self.drawing_density_frame.grid_columnconfigure(
            0,
            weight=2,
        )
        self.drawing_density_frame.grid_columnconfigure(
            1,
            weight=1,
        )

    # LEFT FRAME

    def create_drawing_density_label(self, parent):
        self.drawing_density_label = Tkinter.Label(
            parent,
            text=DRAWING_DENSITY_TEXT,
            padx=LABEL_PADX,
            pady=LABEL_PADY,
        )
        self.drawing_density_label.grid(
            row=0,
            column=0,
        )

    # RIGHT FRAME

    def create_drawing_density_combobox(self, parent):
        self.drawing_density_combobox = Pmw.ComboBox(
            parent,
            scrolledlist_items=DENSITY_OPTIONS,
            listheight=COMBOBOX_HEIGHT,
            entryfield_entry_state="readonly",
            selectioncommand=self.set_drawing_density,
        )
        self.drawing_density_combobox.grid(
            row=0,
            column=1,
        )

    # EVENTS

    def set_drawing_density(self, _val):
        value = float(_val)/100
        self.controller.set_drawing_density(value)


"""

    Ladder Visualisation type class view

"""

class LadderVisualisationView(VisualisationTypeView):

    def __init__(self, parent, controller):
        super(LadderVisualisationView, self).__init__(
            parent,
            controller,
        )
        self.create_advanced_view()

    def create_advanced_view(self):
        self.create_advanced_options_label_frame(self.display_option_label_frame)
        self.create_drawing_types_options(self.advanced_options_label_frame)

# ADVANCED OPTIONS =========================

    def create_advanced_options_label_frame(self, parent):
        self.advanced_options_label_frame = Tkinter.LabelFrame(
            parent,
            text=ADVANDED_OPTIONS_TEXT,
            padx=LABEL_PADX,
            pady=LABEL_PADY,
        )
        self.advanced_options_label_frame.pack(
            fill="x",
        )

# DRAWING TYPES ============================

    def create_drawing_types_options(self, parent):
        self.create_drawing_types_frame(parent)
        self.create_drawing_types_radiobuttons(self.drawing_types_frame)

    def create_drawing_types_frame(self, parent):
        self.drawing_types_frame = Tkinter.LabelFrame(
            parent,
            text=DRAWING_TYPES_TEXT,
            padx=LABEL_PADX,
            pady=LABEL_PADY,
        )
        self.create_drawing_types_radiobuttons(self.drawing_types_frame)
        self.drawing_types_frame.pack(
            fill="x",
        )

    def create_drawing_types_radiobuttons(self, parent):
        self.drawing_types_radiobuttons = Tkinter.Frame(
            parent,
        )
        self.config_drawing_types_radiobuttons(self.drawing_types_radiobuttons)
        self.drawing_types_radiobuttons.grid(
            row=0,
            column=0,
            sticky="w",
        )

    def config_drawing_types_radiobuttons(self, parent):
        self.drawing_type_value = Tkinter.IntVar(parent)
        self.drawing_type_value.set(1)

        for text, val in DRAWING_TYPES:
            Tkinter.Radiobutton(
                parent,
                text=text,
                variable=self.drawing_type_value,
                command=self.change_drawing_type_value,
                value=val,
            ).pack(
                anchor="w",
            )

    def change_drawing_type_value(self):
        value = self.drawing_type_value.get()
        self.controller.change_drawing_type(value)


"""

    Sticks Visualisation type class view

"""

class SticksVisualisationView(VisualisationTypeView):

    def __init__(self, parent, controller):
        super(SticksVisualisationView, self).__init__(
            parent,
            controller,
        )
        self.create_advanced_view()

    def create_advanced_view(self):
        pass


"""

    Only for view tests
    
"""

# TESTS ====================================
# best_controller = displayRestraintsControllers.DisplayRestraintsController()
# root = Tkinter.Tk()
# root.title("Test")
# DisplayRestraintsView(root, best_controller)
# root.mainloop()