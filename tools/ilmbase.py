# Copyright (C) 2015~  Gaetan Guidet
#
# This file is part of excons.
#
# excons is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2.1 of the License, or (at
# your option) any later version.
#
# excons is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301,
# USA.

from SCons.Script import *
import excons
import os

def GetOptionsString():
   return """ILMBASE OPTIONS
  with-ilmbase=<path>     : IlmBase prefix
  with-ilmbase-inc=<path> : IlmBase headers directory   [<prefix>/include]
  with-ilmbase-lib=<path> : IlmBase libraries directory [<prefix>/lib]
  ilmbase-static=0|1      : Link static libraries       [0]
  ilmbase-suffix=<str>    : IlmBase library suffix      ['']

  with-ilmbase-python=<path>     : PyIlmBase prefix
  with-ilmbase-python-inc=<path> : PyIlmBase headers directory   [<prefix>/include]
  with-ilmbase-python-lib=<path> : PyIlmBase libraries directory [<prefix>/lib]
  ilmbase-python-suffix=<str>    : PyIlmBase library suffix      ['']"""

def Require(ilmthread=None, iexmath=None, python=None, halfonly=False):
   
   if not halfonly:
      if ilmthread is None:
         ilmthread = (excons.GetArgument("ilmbase-thread", 1, int) != 0)

      if iexmath is None:
         iexmath = (excons.GetArgument("ilmbase-iexmath", 1, int) != 0)

      if python is None:
         python = (excons.GetArgument("ilmbase-python", 0, int) != 0)
   
   else:
      ilmthread = False
      iexmath = False
      python = False

   def _RealRequire(env):
      ilmbase_libsuffix = excons.GetArgument("ilmbase-suffix", "")
      
      # Add python bindings first
      if python:
         pyilmbase_inc, pyilmbase_lib = excons.GetDirs("ilmbase-python")
         
         pyilmbase_libsuffix = excons.GetArgument("ilmbase-python-suffix", ilmbase_libsuffix)
         
         if pyilmbase_inc:
            if not pyilmbase_inc.endswith("OpenEXR"):
               pyilmbase_inc += "/OpenEXR"
            env.Append(CPPPATH=[pyilmbase_inc, os.path.dirname(pyilmbase_inc)])
         
         if pyilmbase_lib:
            env.Append(LIBPATH=[pyilmbase_lib])
         
         env.Append(LIBS=["PyImath" + pyilmbase_libsuffix])
      
      
      ilmbase_inc, ilmbase_lib = excons.GetDirs("ilmbase")
      
      if ilmbase_inc and not ilmbase_inc.endswith("OpenEXR"):
         ilmbase_inc += "/OpenEXR"
      
      if ilmbase_inc:
         env.Append(CPPPATH=[ilmbase_inc, os.path.dirname(ilmbase_inc)])
      
      if ilmbase_lib:
         env.Append(LIBPATH=[ilmbase_lib])
      
      static = (excons.GetArgument("ilmbase-static", 0, int) != 0)

      if sys.platform == "win32" and not static:
         env.Append(CPPDEFINES=["OPENEXR_DLL"])
      
      if ilmthread:
         # ilmthread will be False if halfonly is True
         libname = "IlmThread%s" % ilmbase_libsuffix
         if not static or not excons.StaticallyLink(env, libname):
            env.Append(LIBS=[libname])
      
      if not halfonly:
         libname = "Imath%s" % ilmbase_libsuffix
         if not static or not excons.StaticallyLink(env, libname):
            env.Append(LIBS=[libname])
      
      if iexmath:
         # iexmath will be False if halfonly is True
         libname = "IexMath%s" % ilmbase_libsuffix
         if not static or not excons.StaticallyLink(env, libname):
            env.Append(LIBS=[libname])
      
      if not halfonly:
         libname = "Iex%s" % ilmbase_libsuffix
         if not static or not excons.StaticallyLink(env, libname):
            env.Append(LIBS=[libname])
      
      libname = "Half%s" % ilmbase_libsuffix
      if not static or not excons.StaticallyLink(env, libname):
         env.Append(LIBS=[libname])
      
      excons.AddHelpOptions(ilmbase=GetOptionsString())
   
   return _RealRequire
