#!/usr/bin/python	
"""
DSL for handling conversion of git repository
By Jacob Salomonsen

BNF for language:
setup ::= (path)
command ::= operation | operation path | operation path path
operation = alpha+
path ::= alpha+
"""

from pyparsing import *
import sys
import commands
import subprocess
import os
import shutil

operation = Word ( alphas )
path = Word ( alphanums + '-/.*' )
setup = Literal( '(' ) + path + Literal( ')' ) + LineEnd()
command = operation + LineEnd() | operation + path + LineEnd() | operation + path + path + LineEnd()

root = ""

def main(argv):
	f = open(argv[0], 'r')
	string = f.read()
	setupToken = interpretSetup( setup.parseString( string ) )
	interpretCommands( command.searchString( string ) )

def interpretSetup(setup):
	global root
	root = setup[1]
	print "Root is ", root

def interpretCommands(commands):
	for command in commands:
		print command
		if command[0] == 'gitmv':
			pr = subprocess.Popen( "git mv " + command[1] + " " + command[2], cwd = os.path.dirname( root ), shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			pr.wait()
			#printProcessError(pr)
		if command[0] == 'mv':
			os.rename( root + command[1], root + command[2] )
		if command[0] == 'mkdir':
			if not os.path.exists( command[1] ):
				os.makedirs( root + command[1] )
		if command[0] == 'cp':
			shutil.copy( root + command[1], root + command[2] )
		if command[0] == 'cpdir':
			shutil.copytree( root + command[1], root + command[2] )
		if command[0] == 'reset':
			pr1 = subprocess.Popen( "git reset --hard", cwd = os.path.dirname( root ), shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			pr1.wait()
			pr2 = subprocess.Popen( "git clean -fdx", cwd = os.path.dirname( root ), shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			pr2.wait()
			#printProcessError(pr1)
			#printProcessError(pr2)
			
def printProcessError(process):
	(out, error) = process.communicate()
	print "Error : " + str(error)
	print "out : " + str(out)

if __name__ == "__main__":
	main(sys.argv[1:])