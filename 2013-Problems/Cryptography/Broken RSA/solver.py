#!/usr/bin/python
#http://hacktracking.blogspot.com/2014/03/picoctf-2k13-broken-rsa.html

import time,sys,socket,re,gmpy,collections

HOST = sys.argv[1]
PORT = int(sys.argv[2])
NC   = 3
NM   = 3

cf = []
n  = []

def egcd(a, b):
 if a == 0:
  return (b, 0, 1)
 else:
  g, y, x = egcd(b % a, a)
  return (g, x - (b // a) * y, y)

def modinv(a, m):
 g, x, y = egcd(a, m)
 if g != 1:
  return None  # modular inverse does not exist
 else:
  return x % m

def chinese_remainder_theorem(cf, n):
 if coprime(n):
  a0 = n[1] * n[2]
  a1 = n[0] * n[2]
  a2 = n[0] * n[1]
  b0 = modinv(a0, n[0])
  b1 = modinv(a1, n[1])
  b2 = modinv(a2, n[2])
  c0 = cf[0]
  c1 = cf[1]
  c2 = cf[2]
  return ((a0 * b0 * c0) + (a1 * b1 * c1) + (a2 * b2 * c2)) % (n[0] * n[1] * n[2])
 else:
  return 'The numbers are not coprimes'

def coprime(n):
 l = len(n)
 for i in range(l):
  a = i % l 
  b = (i + 1) % l
  if gmpy.gcd(n[a], n[b]) != 1:
   return False
 return True
 
class Connection:
 def __init__(self, h, p, nm):
  self.sleep = 0.2
  self.size = 50
  self.nm = nm
  self.message = []
  self.i_message = []
  for i in range(self.nm):
   s = str(i) * self.size
   self.message.append(s)
   self.i_message.append(self.m_to_int(s))
  self.server_socket = (h, p)
 def connect(self):
  self.cmessage = [ '', '', '' ]
  self.i_cmessage = [ '', '', '' ]
  self.cflag = ''
  self.n = ''
  self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  self.client.connect(self.server_socket)
 def get_cipher_flag(self):
  #self.client.recv(1024)
  time.sleep(self.sleep)
  self.cflag = int(re.search('0x.*', self.client.recv(1024)).group(0)[2:-1], 16)
  print 'cflag = ', self.cflag
 def get_cipher_message(self, num):
  self.client.send(self.message[num]+"\n")
  #self.client.recv(1024)
  time.sleep(self.sleep)
  self.cmessage[num] = re.search('0x.*', self.client.recv(1024)).group(0)
  self.i_cmessage[num] = self.cm_to_int(self.cmessage[num])
 def m_to_int(self, s):
  exp = 3
  return pow(int(s.encode('hex'), 16), exp)
 def cm_to_int(self, s):
  return int(s[2:-1], 16)
 def get_gcd(self):
  c = collections.Counter()
  for i in range(self.nm):
   n = i % self.nm 
   m = (i + 1) % self.nm
   c[gmpy.gcd(self.i_message[n] - self.i_cmessage[n], self.i_message[m] - self.i_cmessage[m])] += 1
  n = c.most_common(1)[0]
  if n[0] > 1:
   print 'n     = ', n[0]
   self.n = gmpy.mpz(n[0])
 def disconnect(self):
  self.client.close()

c = Connection(HOST, PORT, NM)
for i in range(NC):
 c.connect()
 c.get_cipher_flag()
 for j in range(NM):
  c.get_cipher_message(j)
 c.get_gcd()
 cf.append(c.cflag)
 n.append(c.n)
 c.disconnect()

crt = chinese_remainder_theorem(cf, n)
print hex(int(gmpy.mpz(crt).root(3)[0]))[2:-1].decode('hex')
'''
# ./crack_rsa.py
cflag =  183432220267576292492132231787500365567429443254723902370093717268660821440942897692891409209336083625860622526532735669405478985976131391373638097071941387759145613334518590037634953987431887257447884479468348868961
n     =  135953784270768443683613403195167981915031252138094570429369041989727851055124422396867423943809003975436286026628304014780104754769108750066849076612355407811413680217618966981934851066430783270443526817656919939971313423309707876858646782024226363140350626824949333424034972566150688727067529487352636390043
cflag =  183432220267576292492132231787500365567429443254723902370093717268660821440942897692891409209336083625860622526532735669405478985976131391373638097071941387759145613334518590037634953987431887257447884479468348868961
n     =  147426225645417139553342358404886645198529522490352691359839782491873450611461887111145469995954618522250637992779925978401830015610097593122018203880703073585636063945771347245716348603489552232317048688060505292755946373819909981955997660918014633102382919198924439017502469967016198925492585769516272283379
cflag =  183432220267576292492132231787500365567429443254723902370093717268660821440942897692891409209336083625860622526532735669405478985976131391373638097071941387759145613334518590037634953987431887257447884479468348868961
n     =  627332965352768740770155366254106959845300172492870722009973118834731530296849175221538708067947689697177943580184423563532887600462655450044573132748970903250245024373466833416970187734469135829450190039040909806348483319266202748803421327450659922751634580246585367885974686043464239023205128753870103334908
RSA_isn't_so_great_after_all?!'''