import shutil
import os

source_path = 'assets/analys.gif'
destination_path = 'uploads/'

# Copy image
shutil.copy(source_path, destination_path)

# # Move image (i.e., cut and paste)
# shutil.move(source_path, destination_path)

# # Note: If the destination_path includes a filename, the image will be renamed.

# # Example of moving and renaming the image
# new_filename = 'new_image_name.gif'
# new_destination_path = os.path.join(destination_path, new_filename)
# shutil.move(source_path, new_destination_path)
