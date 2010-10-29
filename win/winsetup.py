from distutils.core import setup
import py2exe


opts = {
    "py2exe": {
    "compressed": 1,
    "optimize": 2,
    "ascii": 1,
    "bundle_files": 1,
    "packages": ["encodings"],
    "dist_dir": "dist"
    }
}

setup  (name = "Gomoz",
       fullname = "Gomoz web scanner",
       version = "1.0.1",
       description = "Gomoz scanner web application",
       author = "Handrix",
       author_email = "securfox@gmail.com",
       url = "http://www.sourceforge.net/projects/gomoz/",
       license = "GPL",
       keywords = ["scanner", "web application", "securfox", "wxPython"],
       windows = [{"script": "gomoz"}],
       options = opts,
       zipfile = None
       )
       
