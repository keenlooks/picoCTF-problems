#!/usr/bin/python
#http://hacktracking.blogspot.com/2014/02/picoctf-2k13-broken-cbc.html

import socket,sys
from Crypto.Cipher import AES

cipher = []
key = []
plain = list('HERE_IS_COMMAND:flag' + ('\x0c' * 12))
count = 0

def oracle_padding(cipher, result = False):
 s = socket.create_connection((sys.argv[1],int(sys.argv[2])))
 s.recv(1024)
 data = ''
 for i in xrange(0,32):
  data = data + chr(cipher[i])
 #print str(data)
 s.sendall(data+"\n")
 recv = s.recv(1024)
 #print recv
 if "Error" in recv:
  return False
 else:
  if result:
   print
   print recv
  return True
 
def oracle_padding_solution(cipher):
 s = socket.create_connection((sys.argv[1],int(sys.argv[2])))
 s.recv(1024)
 data = ''
 for i in xrange(0,32):
  data = data + chr(cipher[i])
 #print str(data)
 s.sendall(data+"\n")
 recv = s.recv(1024)
 #print recv
 if "Invalid" in recv or "Error" in recv or len(recv) < 5:
  return False
 else:
   print
   print recv
   return True

def print_array(a, t, n):
 result = ''
 for i in xrange(0, n):
  result += '%02x' % a[i]
 print t + ' = ' + result

for i in range(32):
 cipher.append(0)
 key.append(0)


for i in range(16):
 for j in range(256):
  count += 1
  cipher[15 - i] = j
  result = oracle_padding(cipher)
  if result:
   key[15 - i] = (i + 1) ^ j
   print '[' + str(i) + ']'
   print_array(cipher, 'c', 16)
   print_array(key, 'k', 16)
   for z in range(i + 1):
    cipher[15 - z] = (i + 2) ^ key[15 - z]
   break

for i in range(16):
 cipher[i] = key[i] ^ ord(plain[16 + i])
print

print_array(cipher, 'solution', 32)
for i in range(256):
 cipher[0]=cipher[0] ^ i
 if oracle_padding_solution(cipher):
   break
   #print "i is:"+str(i)
   #print "cipher char is:"+str(cipher[0])
 cipher[0]=cipher[0] ^ i
print 'Tries = ' + str(count)
'''# ./padding_oracle.py 
[0]
c = 0000000000000000000000000000003b
k = 0000000000000000000000000000003a
[1]
c = 0000000000000000000000000000ee38
k = 0000000000000000000000000000ec3a
[2]
c = 00000000000000000000000000daef39
k = 00000000000000000000000000d9ec3a
[3]
c = 000000000000000000000000fbdde83e
k = 000000000000000000000000ffd9ec3a
[4]
c = 000000000000000000000012fadce93f
k = 000000000000000000000017ffd9ec3a
[5]
c = 000000000000000000007111f9dfea3c
k = 000000000000000000007717ffd9ec3a
[6]
c = 0000000000000000005f7010f8deeb3d
k = 000000000000000000587717ffd9ec3a
[7]
c = 000000000000000071507f1ff7d1e432
k = 000000000000000079587717ffd9ec3a
[8]
c = 000000000000003470517e1ef6d0e533
k = 000000000000003d79587717ffd9ec3a
[9]
c = 000000000000283773527d1df5d3e630
k = 000000000000223d79587717ffd9ec3a
[10]
c = 0000000000be293672537c1cf4d2e731
k = 0000000000b5223d79587717ffd9ec3a
[11]
c = 000000001db92e3175547b1bf3d5e036
k = 0000000011b5223d79587717ffd9ec3a
[12]
c = 0000001d1cb82f3074557a1af2d4e137
k = 0000001011b5223d79587717ffd9ec3a
[13]
c = 0000011e1fbb2c3377567919f1d7e234
k = 00000f1011b5223d79587717ffd9ec3a
[14]
c = 0000001f1eba2d3276577818f0d6e335
k = 000f0f1011b5223d79587717ffd9ec3a
[15]
c = 041f1f0001a5322d69486707efc9fc2a
k = 140f0f1011b5223d79587717ffd9ec3a

solution = 72636e771db92e3175547b1bf3d5e03600000000000000000000000000000000

key: XXX TRY TO READ ME XXX
Tries = 1466'''