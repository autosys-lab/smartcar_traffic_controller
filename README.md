# Traffic Controller
This program controls the speed, lights and switches for the smartcars. Based on a configuratioin file (WIP), different routing options for different vehicle classes can be set.

The controller does both the pathplanning and the path following for all the smartcars tracked by the overhead cameras. It speaks to the smartcars via UDP and to the switch controller, to set the switches in the road.

## Simulation 
This program can also be run in simulation mode for debugging and testing. Set `use_sim=True` in the main.

## Installation
After cloning this repo, run `pipenv install` to install all the dependencies. After that, the `main.py` can be run (either in normal or simulation mode)
