import sys
import math

class LZWBinFa:
    class Csomopont:
        def __init__(self, b='/'):
            self.betu = b
            self.balNulla = None
            self.jobbEgy = None

        def nullasGyermek(self):
            return self.balNulla

        def egyesGyermek(self):
            return self.jobbEgy

        def ujNullasGyermek(self, gy):
            self.balNulla = gy

        def ujEgyesGyermek(self, gy):
            self.jobbEgy = gy

        def getBetu(self):
            return self.betu

    def __init__(self):
        self.gyoker = self.Csomopont('/')
        self.fa = self.gyoker
        self.melyseg = 0
        self.maxMelyseg = 0
        self.atlagosszeg = 0
        self.atlagdb = 0
        self.szorasosszeg = 0.0

    def add_bit(self, b):
        if b == '0':
            if not self.fa.nullasGyermek():
                uj = self.Csomopont('0')
                self.fa.ujNullasGyermek(uj)
                self.fa = self.gyoker
            else:
                self.fa = self.fa.nullasGyermek()
        else:
            if not self.fa.egyesGyermek():
                uj = self.Csomopont('1')
                self.fa.ujEgyesGyermek(uj)
                self.fa = self.gyoker
            else:
                self.fa = self.fa.egyesGyermek()

    def _kiir_rec(self, elem, out_file):
        if elem is not None:
            self.melyseg += 1
            self._kiir_rec(elem.egyesGyermek(), out_file)
            
            out_file.write("-" * (3 * self.melyseg))
            out_file.write(f"{elem.getBetu()}({self.melyseg - 1})\n")
            
            self._kiir_rec(elem.nullasGyermek(), out_file)
            self.melyseg -= 1

    def kiir(self, out_file):
        self.melyseg = 0
        self._kiir_rec(self.gyoker, out_file)

    def _rmelyseg(self, elem):
        if elem is not None:
            self.melyseg += 1
            if self.melyseg > self.maxMelyseg:
                self.maxMelyseg = self.melyseg
            self._rmelyseg(elem.egyesGyermek())
            self._rmelyseg(elem.nullasGyermek())
            self.melyseg -= 1

    def getMelyseg(self):
        self.melyseg = 0
        self.maxMelyseg = 0
        self._rmelyseg(self.gyoker)
        return self.maxMelyseg - 1

    def _ratlag(self, elem):
        if elem is not None:
            self.melyseg += 1
            self._ratlag(elem.egyesGyermek())
            self._ratlag(elem.nullasGyermek())
            self.melyseg -= 1
            if elem.egyesGyermek() is None and elem.nullasGyermek() is None:
                self.atlagdb += 1
                self.atlagosszeg += self.melyseg

    def getAtlag(self):
        self.melyseg = 0
        self.atlagosszeg = 0
        self.atlagdb = 0
        self._ratlag(self.gyoker)
        if self.atlagdb == 0:
            return 0.0
        return self.atlagosszeg / self.atlagdb

    def _rszoras(self, elem, atlag):
        if elem is not None:
            self.melyseg += 1
            self._rszoras(elem.egyesGyermek(), atlag)
            self._rszoras(elem.nullasGyermek(), atlag)
            self.melyseg -= 1
            if elem.egyesGyermek() is None and elem.nullasGyermek() is None:
                self.atlagdb += 1
                self.szorasosszeg += (self.melyseg - atlag) ** 2

    def getSzoras(self):
        atlag = self.getAtlag()
        self.szorasosszeg = 0.0
        self.melyseg = 0
        self.atlagdb = 0
        
        self._rszoras(self.gyoker, atlag)
        
        if self.atlagdb - 1 > 0:
            return math.sqrt(self.szorasosszeg / (self.atlagdb - 1))
        else:
            return math.sqrt(self.szorasosszeg)

def usage():
    print("Usage: python lzwtree.py in_file -o out_file")

def main():
    if len(sys.argv) != 4:
        usage()
        sys.exit(-1)

    in_file_name = sys.argv[1]
    if sys.argv[2] != '-o':
        usage()
        sys.exit(-2)
        
    out_file_name = sys.argv[3]

    try:
        be_file = open(in_file_name, "rb")
    except FileNotFoundError:
        print(f"{in_file_name} nem letezik...")
        usage()
        sys.exit(-3)

    bin_fa = LZWBinFa()

    while True:
        b = be_file.read(1)
        if not b:
            break
        if b[0] == 0x0a:
            break

    kommentben = False

    while True:
        b = be_file.read(1)
        if not b:
            break
        
        val = b[0]

        if val == 0x3e:
            kommentben = True
            continue

        if val == 0x0a:
            kommentben = False
            continue

        if kommentben:
            continue

        if val == 0x4e:
            continue

        for i in range(8):
            if val & 0x80:
                bin_fa.add_bit('1')
            else:
                bin_fa.add_bit('0')
            val = (val << 1) & 0xFF

    be_file.close()

    with open(out_file_name, "w") as ki_file:
        bin_fa.kiir(ki_file)
        ki_file.write(f"depth = {bin_fa.getMelyseg()}\n")
        ki_file.write(f"mean = {bin_fa.getAtlag()}\n")
        ki_file.write(f"var = {bin_fa.getSzoras()}\n")

if __name__ == "__main__":
    main()
