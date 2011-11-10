==================
 README: PyGeo
==================

:Author: Arthur Siegel
:Contact: ajsiegel@optonline.com
:Date: $Date: 2005/31/12 $
:Web-site: http://pygeo.sourceforge.net

Thank you for downloading PyGeo.  

As this is a work in progress, please check the project web site for
updated distributions. 


.. _Python: http://www.python.org/
.. _VPython: http://www.vpython.org/
.. _`Numerical Python`: http://pfdubois.com/numpy/

.. contents::


Dependencies
============+

To run the PyGeo scripts, the following are required 

- Python_ interpreter and development environment

  - Version: 2.4 or later. 
  - download site reference: http://www.python.org/download/.

- VPython_ 3d rendering library for Python

  - Version: compatible with installed Python version 
  - download site reference:  http://www.vpython.org/download.html.
  
- `Numerical Python`_ fast array processing libraries for Python

  - Version: compatible with installed Python and VPython versions 
  - download: included with VPython binary distribution
    
Installation
============

Assumes successful installation of dependencies, as above.


GNU/Linux, Unix, MacOS X, etc.
------------------------------

1. Open a shell.

2. Go to the directory created by expanding the downloaded archive::

       cd <archive_directory_path>

3. Install the package::

       python setup.py install

   If the python executable isn't on your path, you'll have to specify
   the complete path, such as /usr/local/bin/python.  You may need
   root permissions to complete this step.


Windows
-------

1.  Run downloaded self-extracting executable and follow prompts.
2.  Done

Project Directories
===========================


  * pygeo: the project root directory, installed as a Python package.
  * pygeo//base: abstract geometric classes, constants, options, etc.  
  * pygeo/classes_real: implementation of classes and factory functions for the geometry of real number space  
  * pygeo//classes_complex: implementation of classes and factory functions for the geometry of complex number space
  * pygeo//docs_html: pygeo related documentation  
  * pygeo//examples: examples of pygeo constructions
  * pygeo//images: empty directory, default for povray image output
  * pygeo//povout: empty directory, default for povray scene discription file output
  * pygeo//tests: test scripts for implemented classes, called via their facotry functions
  * pygeo//utils: modules providing useful convenience utilites to pygeo



Usage
=====

See docs_html//quickstart.html