import re

from ..Script import Script

class LevelingMeshOptimizer(Script):
    def getSettingDataString(self):
        return """{
            "name": "Leveling Mesh Optimizer",
            "key": "LevelingMeshOptimizer",
            "metadata": {},
            "version": 2,
            "settings": {
                "spacing": {
                    "label": "Spacing",
                    "description": "How far apart to space the probe points within the mesh",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 10
                }
            }
        }"""


    ##  Calculates and fills in the bounds of the first layer.
    #   \param data A list of lines of GCODE representing the entire print.
    #   \return A similar list, with the bounds of the mesh filled in.
    def execute(self, data: [str]) -> [str]:
        _DATA_START_GCODE = 1
        _DATA_LAYER_0 = 2

        # Calculate bounds of first layer
        bounds = self.findBounds(data[_DATA_LAYER_0])

        # Fill in bounds in start GCODE
        data[_DATA_START_GCODE] = self.fillBounds(data[_DATA_START_GCODE], bounds)

        return data


    ##  Finds the minimum and maximum X and Y coordinates in a GCODE layer.
    #   \param data A block of GCODE representing the layer.
    #   \return A dict such that [X|Y][min|max] resolves to a float
    def findBounds(self, data: str) -> {str: {str: float}}:
        bounds = {
            "X": {"min": float("inf"), "max": float("-inf")},
            "Y": {"min": float("inf"), "max": float("-inf")},
        }

        for line in data.split("\n"):
            # Get coordinates on this line
            for match in re.findall(r"([XY])([\d.]+)\s", line):
                # Get axis letter
                axis = match[0]

                # Skip axes we don't care about
                if axis not in bounds:
                    continue

                # Parse parameter value
                value = float(match[1])

                # Update bounds
                bounds[axis]["min"] = min(bounds[axis]["min"], value+6)
                bounds[axis]["max"] = max(bounds[axis]["max"], value+6)

        return bounds


    ##  Replaces the G29 command in the start GCODE so that the bounds are filled in.
    #   \param data The entire start GCODE block.
    #   \return The same GCODE but with the bounds of the mesh filled in.
    def fillBounds(self, data: str, bounds: {str: {str: float}}) -> str:
        # Fill in the level command template
        # new_cmd = "G29 L%.3f R%.3f F%.3f B%.3f \n G0 X1 Y1; Leveling mesh defined by LevelingMeshOptimizer" % (
        new_cmd = "G29 L%.3f R%.3f F%.3f B%.3f \n G0 X1 Y1; Leveling mesh defined by LevelingMeshOptimizer" % (
           bounds["X"]["min"], min([190,bounds["X"]["max"]]),
            bounds["Y"]["min"], min([180,bounds["Y"]["max"]]),
)

        # Replace G29 command in GCODE
        return re.sub(r"^G29 .*$", new_cmd, data, flags=re.MULTILINE)
