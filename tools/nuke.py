# Copyright (C) 2010  Gaetan Guidet
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
import sys

def PluginExt():
  if str(Platform()) == "darwin":
    return ".dylib"
  elif str(Platform()) == "win32":
    return ".dll"
  else:
    return ".so"

def Require(env):
  ndkinc = ARGUMENTS.get("with-nuke-inc", None)
  ndklib = ARGUMENTS.get("with-nuke-lib", None)
  ndkdir = ARGUMENTS.get("with-nuke", None)
  
  if ndkdir:
    if sys.platform == "darwin":
      ndkdir = os.path.join(ndkdir, "Contents", "MacOS")
      if ndkinc is None:
        ndkinc = os.path.join(ndkdir, "include")
      if ndklib is None:
        ndklib = ndkdir
    else:
      if ndkinc is None:
        ndkinc = os.path.join(ndkdir, "include")
      if ndklib is None:  
        ndklib = ndkdir
  
  if ndkinc is None or ndklib is None:
    print("WARNING - You may want to set nuke include/library directories using with-nuke=, with-nuke-inc, with-nuke-lib")

  if ndkinc and not os.path.isdir(ndkinc):
    print("WARNING - Invalid nuke include directory: \"%s\"" % ndkinc)
    return

  if ndklib and not os.path.isdir(ndklib):
    print("WARNING - Invalid nuke library directory: \"%s\"" % ndklib)
    return

  if ndkinc:
    env.Append(CPPPATH=[ndkinc])
  
  if ndklib:
    env.Append(LIBPATH=[ndklib])
  
  if sys.platform == "darwin":
    #env.Append(CCFLAGS=" -isysroot /Developer/SDKs/MacOSX10.4u.sdk")
    #env.Append(LINKFLAGS=" -Wl,-syslibroot,/Developer/SDKs/MacOSX10.4u.sdk")
    #env.Append(LINKFLAGS=" -framework QuartzCore -framework IOKit -framework CoreFoundation -framework Carbon -framework ApplicationServices -framework OpenGL -framework AGL -framework Quicktime")
    pass
  
  env.Append(DEFINES = ["USE_GLEW"])
  if sys.platform != "win32":
    env.Append(CCFLAGS = " -Wno-unused-variable -Wno-unused-parameter")
    env.Append(LIBS = ["DDImage", "GLEW"])
  else:
    env.Append(LIBS = ["DDImage", "glew32"])



