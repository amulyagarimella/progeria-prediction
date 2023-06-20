import os
import subprocess


# convert images to TIF
ims_to_tif_script_path = "TODO"
ims_path = "TODO"
subprocess.Popen(["python", ims_to_tif_script_path, 1], cwd=ims_path)

# run CellProfiler analysis pipeline
# https://github.com/CellProfiler/CellProfiler/wiki/Getting-started-using-CellProfiler-from-the-command-line