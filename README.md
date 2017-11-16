# PyRy3D-DisplayRestraints

Extension for creating visualizations of distance restraints in PyRy3D Chimera Extension

## Installation

1. Install UCSF Chimera and PyRy3D Chimera Extension - http://genesilico.pl/pyry3d/installing#gui-installation
2. Download PyRy3D-DisplayRestraints (alpha branch is always stable version, if you want the newest code clone *development* branch).
3. Unzip files.
4. Copy files from PyRy3D-DisplayRestraints folder to your_chimera_localization/share/PyRy3D_Extension/ (PyRy_Results file must be replaced!)
5. Extension is now integrated with PyRy3D Chimera Extension.You can run it from Results Menu (available after running PyRy3D Simulation or Complex Scoring) by choosing Display Restraints.

## Infrastructure

The application is intended to be split in two separate extensions and a core layer. First of them (which already exists in alpha version) is a part of PyRy3D Chimera Extension. Second one will be a standalone application for UCSF Chimera. The common part of both of them will be a core layer.

### Display Restraints Core [alpha-stable]

Core part of the project provides application logic, necessary mechanisms and methods. In itself it is not an extension, it contains only the required features to build a gui part.
Display Restraints Core was separated to allow for parallel development of the two separate extensions.

### Display Restraints for PyRy3D [alpha-stable]

Extension which is inseparable from PyRy3D Chimera Extension. Uses data and models used for modeling in PyRy3D.

### Display Restraints Chimera Extension [DEVELOPMENT IN PROGRESS]

An independent extension for UCSF Chimera. Allows you to load any macromolecular model, distance restraints and shows visualization for this set of data.

## Feedback

Extension is still in alpha version, so feel free to write about your experiences using Display Restraints or report bugs through https://kubawajs.github.io contact section.

## Known bugs

- [ ] Connections between chains from the wrong sides

## Logs

> 0.1.0
>> Latest stable version 0.1 pushed to branch development


----------

### Version information

v. 0.1 development
