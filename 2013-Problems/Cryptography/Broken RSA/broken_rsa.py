#!/usr/bin/env python

import time,sys,os
from Crypto.PublicKey import RSA

flag = open("flag", "r").read()
n = getattr(RSA.generate(1024,os.urandom),'n')

welcome = """
*******************************************
***             Welcome to the          ***
***    FlAg EnCrYpTiOn SeRviCe 9000!    ***
*******************************************

We encrypt the flags, you get the points!
"""


print (welcome)
sys.stdout.flush()

#no one will ever be able to solve our super challenge!
print "To prove how secure our service is "
print ("here is an encrypted flag:\n")
print ("==================================\n")
print (hex(pow(int(flag.encode("hex"), 16),3,n)))
print ("\n==================================\n")
print ("Find the plaintext and we'll give you points\n\n")
sys.stdout.flush()
while 1:
  print ("\nNow enter a message you wish to encrypt: ")
  sys.stdout.flush()
  m = raw_input()
  print ("Your super unreadable ciphertext is:\n")
  print ("==================================\n")
  print (hex(pow(int(m.encode("hex"), 16),3,n))) 
  print ("\n==================================\n")
  sys.stdout.flush()