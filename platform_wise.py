#platform_wise.py

"""
The MIT License

Copyright (c) 2012 Umer Mansoor <umermk3@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

"""
A script which returns information about the system like system memory, number 
of cores, etc.Currently, this script supports FreeBSD, Linux, OSX and SunOS. 

I wrote this script to help in writing startup scripts for our in house Java 
application. I wanted to calculate system memory to determine an optimal heap 
size, number of cores to set the thread pool size and to determine whether the 
current system can run the Java application or not.
"""

import subprocess
import re
import string
import os

class System:
	
	def __init__(self):
		# Build the command to run Java
		self.java = os.environ.get('JAVA_HOME') # Check if the enviroment for java home folder is set
		if self.java is not None:
			self.java = self.java + "/bin/java"
		else:
			self.java = "java"
		
	def getJavaVersion(self):
		"""Returns the verion of Java as a string
		"""
		return subprocess.check_output([self.java + " -version 2>&1 | awk -F'\"' 'NR==1 {print $2}'"], shell=True).strip()
		
	def getJavaVendor(self):
		"""Returns the Java Vendor
		"""
		vendor = subprocess.check_output([self.java + " -version 2>&1 | awk 'NR==2 {print $1}'"], shell=True).strip()		
		if "OpenJDK" in vendor:
			return "OpenJDK"
		elif "Java(TM)" in vendor:
			return "Oracle"
		return "Other"
			
	def getJavaArchitecture(self):
		"""Returns either 64-bit or 32-bit depending on the Java version
		"""
		if self.getJavaVendor() == "OpenJDK":
			return subprocess.check_output([self.java + " -version 2>&1 | awk 'NR==3 {print $2}'"], shell=True).strip()
		elif self.getJavaVendor() == "Oracle":	
			return subprocess.check_output([self.java + " -version 2>&1 | awk 'NR==3 {print $3}'"], shell=True).strip()
		return "Unknown"
		
	def getSystemMemoryInMB(self):
		"""Returns the amount of memory in megabytes.
		"""
		if self.isLinux():
			return subprocess.check_output(["free", "-m"]).strip().split()[7]
		elif self.isDarwin() or self.isFreeBSD():
			#TODO: Have to check the FreeBSD stuff, not sure if it will work
			memInBytes = subprocess.check_output(["sysctl", "hw.memsize"]).strip().split()
			return int(memInBytes[1])/(1024 * 1024) # Covert to megabytes and return
		elif self.isSunOS():
			#TODO: Test on SunOS
			return subprocess.check_output(["prtconf | awk '/Memory size:/ {print $3}'"], shell=True).strip()
		return None
		
	def getNumberOfCPUCores(self):
		"""Returns the number of CPU cores
		"""
		if self.isLinux(): # Use the Regular Expression this time for a change
			f = open('/proc/cpuinfo', 'r')
			i = 0
			for line in f:
				if re.search("processor\s*:", line):
					i = i + 1
			f.close()
			return i
		elif self.isDarwin() or self.isFreeBSD():
			return subprocess.check_output(["sysctl","hw.ncpu"]).strip().split()[1]
		elif self.isSunOS(): #TODO: Test this
 			return subprocess.check_output(["psrinfo | wc -l"], shell=True).strip()
		return None
		
	def getSystemName(self):
		"""Returns the system name. It gets the output of the uname command
		"""
		return subprocess.check_output(["uname"]).strip()
		
	def isLinux(self):
		"""Returns true if the host system is Linux
		"""
		sysname = self.getSystemName()
		
		if "Linux" in sysname:
			return True
		else:
			return False
		
	def isOSX(self):
		"""Returns true if the host system is Darwin (OSX)
		"""
		return self.isDarwin()
		
	def isDarwin(self):
		"""Returns true if the host system is Darwin (OSX)
		"""
		sysname = self.getSystemName()

		if "Darwin" in sysname:
			return True
		else:
			return False
	
	def isFreeBSD(self):
		"""Returns true if the host system is FreeBSD
		"""
		sysname = self.getSystemName()

		if "FreeBSD" in sysname:
			return True
		else:
			return False
	
	def isSunOS(self):
		"""Returns true if the host system is SunOS
		"""
		sysname = self.getSystemName()

		if "SunOS" in sysname:
			return True
		else:
		    return False
		
def main():
	"""Executes the function in the System class
	"""
	print "====== System Information ======"
	sysInfo = System()
	
	print "System Type: %s" % sysInfo.getSystemName()
	print "Number of CPU Cores: %s" % sysInfo.getNumberOfCPUCores()
	print "System Memory: %s MB" % sysInfo.getSystemMemoryInMB()
	
	print "Linux Based: %s" % sysInfo.isLinux()
	print "Free BSD Based: %s" % sysInfo.isFreeBSD()
	print "OSX (Darwin): %s" % sysInfo.isOSX()
	print "SunOS Compatible: %s" % sysInfo.isSunOS()
	
	
	
	print "Java Vendor: %s" % sysInfo.getJavaVendor()
	print "Java Version: %s" % sysInfo.getJavaVersion()
	print "Java Architecture: %s" % sysInfo.getJavaArchitecture()
	
if __name__ == '__main__':
	main()
	
	
