#!/usr/bin/env python
import os,sys
from Crypto.Cipher import AES
import time


#actual key and iv go here...
flag = open("flag", "r").read()
key = open("key", "r").read().strip().decode("hex")
iv  = open("iv", "r").read().strip().decode("hex")

def pkcs(msg):
  print msg.encode("hex")
  padding_length = ord(msg[-1])
  padding = msg[-padding_length:]
  print padding.encode("hex")
  if (padding != (chr(padding_length)*padding_length)):
    print (chr(padding_length)*padding_length).encode("hex")
    return None
  return msg[:-padding_length]

def decrypt(cipher,enc):
  #print enc,((len(enc) % 16) != 0)
  dec = ""
  if ((len(enc) % 16) != 0):
    return (False,"Error: cipher length must be a multiple of 16\n")
  dec = cipher.decrypt(enc)
  msg = pkcs(dec)
  if msg is None:
    return (False,"Error: incorrect padding\n")
  return (True,msg)

def process(cmd):
  # Message is like HERE_IS_COMMAND:cmd
  # eg "HERE_IS_COMMAND:help"
  oldcmd = cmd
  cmd = cmd[16:] #ignore the COMMAND: part, it's all the same anyhow
  
  if (cmd == "help"):
    return "Commands:\n\thelp - this\n\tflag - prints out the flag\n\tnyan - prints out a nyan cat\n"
  if (cmd == "flag"):
    return flag
  if (cmd == "nyan"):
    return """
+      o     +              o   
    +             o     +       +
o          +
    o  +           +        +
+        o     o       +        o
-_-_-_-_-_-_-_,------,      o 
_-_-_-_-_-_-_-|   /\_/\  
-_-_-_-_-_-_-~|__( ^ .^)  +     +  
_-_-_-_-_-_-_-""  ""      
+      o         o   +       o
    +         +
o        o         o      o     +
    o           +
+      +     o        o      +    
"""
  return "Invalid command. See help for a list of commands: ["+oldcmd+"]"


welcome = """
Enter your encrypted command:
"""
print welcome
sys.stdout.flush()
while 1:
  m = raw_input()
  cipher = AES.new(key, AES.MODE_CBC, iv)
  success,cmd = decrypt(cipher,m)
  if (success):
    print process(cmd)
  else:
    print cmd
  sys.stdout.flush()