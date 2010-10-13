from distutils.core import setup
import py2exe


setup  (name = "Gomoz",
       fullname = "Card credit checker",
       version = "1.0.1",
       description = "Card credit check",
       author = "Ali MEZGANI",
       author_email = "handrix@users.sourceforge.net",
       url = "http://www.sourceforge.net/projects/cc-checker/",
       license = "GPL",
       keywords = ["card credit software", "visa", "master card", "wxPython"],
       scripts = ["main.py"]
       )

