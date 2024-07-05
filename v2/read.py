import os
from PIL import ImageGrab
import io


class SolutionDB:
    db_path = ""
    
    def __init__(self):
        pass
        
 
class InputReader:
    def __init__(self):
        pass
    
    def from_image(self):
        """ reads an image and uses image recognition to convert it
            to a compatible list
        """
        pass
    
    def from_text(self):
        """ reads a variety of formats and converts it to a
            compatible list
        """
        pass
    
    def from_clipboard(self):
        """ Pulls either text or image from the clipboard and coverts
            it to a compatible list
        """
        img = ImageGrab.grabclipboard()
        pass
    
    def from_file(self):
        """ Reads a text or image from a file and coverts it to a
            compatible list
        """
        pass

