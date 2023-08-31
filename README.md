# Adaptive-Mesh-Levelling-Cura
Adaptive Mesh Levelling Cura Marlin Firmware
This is a tested python script to be used in Cura for Adaptive Bed Mesh levelling in Marlin Firmware 3D printers.  This script get the bounding box of items  on the Cura Bed and apply the mesh bed levelling with offset of 6mm.  The G29 must be present in Start Gcode portion of Cura. This G29 is replaced by the G29 LFRB with values of the calculated bounding box. This can be changed in by Editing the python file.
a- copy the the attached Python file and place in  in Script folder of Cura. C:\Users\Administrator\AppData\Roaming\cura\5.4\scripts
b- In your Start Gcode G29 must be placed after G28.
c- In Cura MENU select Extensions---Post Processing---Modify Gcode  and then select from Drop Down Menu the script with name Leveling Mesh Optimizer , the spacing value 10mm doesnt have any effect and reserve for future use. 
d- Now add your parts to be 3d printed and save the file... In the file you will find G29 L15.275 R190.000 F15.275 B180.000  the values infront of LRFB are calculated bounding box with 6mm skirt offset.
Test and Enjoy.
https://www.youtube.com/watch?v=QksjSpTgaGU
