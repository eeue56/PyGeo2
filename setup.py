
#!/usr/bin/env python

# To use:
#       python setup.py install
#

# thanks to docutils setup.py


import sys
import os
import glob
from distutils.core import setup
from distutils.command.build_py import build_py
from distutils.command.install_data import install_data

from distutils.core import setup

__docformat__ = 'restructuredtext'
__version__ = '1.0a1'



class smart_install_data(install_data):

    # From <http://wiki.python.org/moin/DistutilsInstallDataScattered>,
    # by Pete Shinners.

    def run(self):
        #need to change self.install_dir to the library dir
        install_cmd = self.get_finalized_command('install')
        self.install_dir = getattr(install_cmd, 'install_lib')
        return install_data.run(self)


doc_files=[]
for root, dirs, files in os.walk(os.path.join('pygeo','docs_html')):
    doc_files.append((root, [os.path.join(root,file) for file in files]))


def do_setup():
    kwargs = package_data.copy()
    if sys.hexversion >= 0x02030000:    # Python 2.3
        kwargs['classifiers'] = classifiers
    else:
        kwargs['cmdclass'] = {'build_py': dual_build_py}
    dist = setup(**kwargs)
    return dist

package_data= {'name':'PyGeo',
      'version':'1.0a1',
      'description':'PyGeo - 3d Dynamic Geometry Toolkit',
      'author':'Arthur J. Siegel',
      'author_email':'ajsiegel@optonline.com',
      'platforms': 'OS-independent',
      'cmdclass': {'install_data': smart_install_data},
      'url':'http://pygeo.sourceforge.net',
      'license':'GPL',
      'packages':['pygeo','pygeo.base','pygeo.classes_real','pygeo.classes_complex','pygeo.utils',
      'pygeo.classes_real.points','pygeo.classes_real.lines','pygeo.tests', 'pygeo.tests.real',
      'pygeo.tests.complex','pygeo.examples.real','pygeo.examples.complex', 'pygeo.examples.lawrence',
      'pygeo.povout','pygeo.images'],

      'package_data':{'pygeo': [os.path.join('pygeo','help.txt')]},
      'data_files':[('pygeo', [os.path.join('pygeo','help.txt')]),] + doc_files,

      'long_description':"""
      PyGeo is a 3d dynamic geometry toolkit written in Python, with dependencies on
      Numeric Python, which provides fast multi-dimensional array processing and
      VPython, which provides the 3d graphics rendering.
      """
     }



classifiers = ['Programming Language :: Python',
    'Development Status :: 3 - Alpha',
    'Environment :: Win32 (MS Windows)',
    'Environment :: X11 Applications',
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'Requires :: visual',
    'Requires :: Numeric',
    'Requires-Python :: >=2.3' ,
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Copyright:: Arthur Siegel, 2001',
    'Natural Language :: English',
    'Topic :: Education',
    'Topic :: Education :: Computer Aided Instruction (CAI)',
    'Topic :: Scientific/Engineering :: Mathematics'
    'Operating System :: POSIX'
    'Operating System :: Microsoft :: Windows']
    

class dual_build_py(build_py):

    """
    This class allows the distribution of both packages *and* modules with one
    call to `distutils.core.setup()` (necessary for pre-2.3 Python).  Thanks
    to Thomas Heller.
    """

    def run(self):
        if not self.py_modules and not self.packages:
            return
        if self.py_modules:
            self.build_modules()
        if self.packages:
            self.build_packages()
#        self.byte_compile(0)


if __name__ == '__main__' :
    do_setup()
