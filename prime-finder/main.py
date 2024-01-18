# Denis Kotnik

import math

# N-ti koren
def nth_root(val, n):
    ret = int(val**(1./n))
    return ret + 1 if (ret + 1) ** n == val else ret

# Generator za prastevila skopiran z neta.
# (Uporabi se memoizacijo?)
class prime_list():
    def __init__(self):
        self.primelst = [2] # Prvo prastevilo
        self.n = 2 # Prvo prastevilo

    def increment(self):
        self.n += 1
        candidate = self.primelst[-1]+1
        limit = int(math.floor(math.sqrt(candidate)))
        prime = True
        while True:
            for p in self.primelst:
                if p > limit:
                    break
                if (candidate % p) == 0:
                    prime = False
                    break
            if prime:
                self.primelst.append(candidate)
                return
            else:
                candidate += 1
                limit = int(math.floor(math.sqrt(candidate)))
                prime = True

max = 500000
rezultati = []
rezultati = set(rezultati) # Mnozica (hashtable)

vsota = 0

a = prime_list()
while(nth_root(max, 2) >= a.primelst[-1]):
    b = prime_list()
    while(nth_root(max, 3) >= b.primelst[-1]):
        c = prime_list()
        while(nth_root(max, 4) >= c.primelst[-1]):
            vsota = a.primelst[-1]**2 + b.primelst[-1]**3 + c.primelst[-1]**4
            if (vsota < max and vsota not in rezultati): # Uporabi neko drevo
                rezultati.add(vsota)
            c.increment()
        b.increment()
    a.increment()
    
print('Stevilo rezultatov: ', len(rezultati))