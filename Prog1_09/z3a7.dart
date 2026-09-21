import 'dart:io';
import 'dart:math' as math;

class Csomopont {
  String betu;
  Csomopont? balNulla;
  Csomopont? jobbEgy;

  Csomopont([this.betu = '/']);

  Csomopont? nullasGyermek() => balNulla;
  Csomopont? egyesGyermek() => jobbEgy;

  void ujNullasGyermek(Csomopont gy) {
    balNulla = gy;
  }

  void ujEgyesGyermek(Csomopont gy) {
    jobbEgy = gy;
  }

  String getBetu() => betu;
}

class LZWBinFa {
  late Csomopont gyoker;
  late Csomopont fa;

  int melyseg = 0;
  int maxMelyseg = 0;
  int atlagosszeg = 0;
  int atlagdb = 0;
  double szorasosszeg = 0.0;

  LZWBinFa() {
    gyoker = Csomopont('/');
    fa = gyoker;
  }

  void addBit(String b) {
    if (b == '0') {
      if (fa.nullasGyermek() == null) {
        Csomopont uj = Csomopont('0');
        fa.ujNullasGyermek(uj);
        fa = gyoker;
      } else {
        fa = fa.nullasGyermek()!;
      }
    } else {
      if (fa.egyesGyermek() == null) {
        Csomopont uj = Csomopont('1');
        fa.ujEgyesGyermek(uj);
        fa = gyoker;
      } else {
        fa = fa.egyesGyermek()!;
      }
    }
  }

  void _kiirRec(Csomopont? elem, StringSink os) {
    if (elem != null) {
      melyseg++;
      _kiirRec(elem.egyesGyermek(), os);

      os.write("-" * (3 * melyseg));
      os.write("${elem.getBetu()}(${melyseg - 1})\n");

      _kiirRec(elem.nullasGyermek(), os);
      melyseg--;
    }
  }

  void kiir(StringSink os) {
    melyseg = 0;
    _kiirRec(gyoker, os);
  }

  void _rmelyseg(Csomopont? elem) {
    if (elem != null) {
      melyseg++;
      if (melyseg > maxMelyseg) {
        maxMelyseg = melyseg;
      }
      _rmelyseg(elem.egyesGyermek());
      _rmelyseg(elem.nullasGyermek());
      melyseg--;
    }
  }

  int getMelyseg() {
    melyseg = 0;
    maxMelyseg = 0;
    _rmelyseg(gyoker);
    return maxMelyseg - 1;
  }

  void _ratlag(Csomopont? elem) {
    if (elem != null) {
      melyseg++;
      _ratlag(elem.egyesGyermek());
      _ratlag(elem.nullasGyermek());
      melyseg--;
      if (elem.egyesGyermek() == null && elem.nullasGyermek() == null) {
        atlagdb++;
        atlagosszeg += melyseg;
      }
    }
  }

  double getAtlag() {
    melyseg = 0;
    atlagosszeg = 0;
    atlagdb = 0;
    _ratlag(gyoker);
    if (atlagdb == 0) return 0.0;
    return atlagosszeg / atlagdb;
  }

  void _rszoras(Csomopont? elem, double atlag) {
    if (elem != null) {
      melyseg++;
      _rszoras(elem.egyesGyermek(), atlag);
      _rszoras(elem.nullasGyermek(), atlag);
      melyseg--;
      if (elem.egyesGyermek() == null && elem.nullasGyermek() == null) {
        atlagdb++;
        szorasosszeg += (melyseg - atlag) * (melyseg - atlag);
      }
    }
  }

  double getSzoras() {
    double atlag = getAtlag();
    szorasosszeg = 0.0;
    melyseg = 0;
    atlagdb = 0;

    _rszoras(gyoker, atlag);

    if (atlagdb - 1 > 0) {
      return math.sqrt(szorasosszeg / (atlagdb - 1));
    } else {
      return math.sqrt(szorasosszeg);
    }
  }
}

void usage() {
  print("Usage: dart lzwtree.dart in_file -o out_file");
}

void main(List<String> args) async {
  if (args.length != 4) {
    usage();
    exit(-1);
  }

  String inFile = args[0];
  if (args[1] != '-o') {
    usage();
    exit(-2);
  }
  String outFile = args[2];

  File beFile = File(inFile);
  if (!await beFile.exists()) {
    print("$inFile nem letezik...");
    usage();
    exit(-3);
  }

  List<int> bytes = await beFile.readAsBytes();
  LZWBinFa binFa = LZWBinFa();

  int idx = 0;
  while (idx < bytes.length) {
    int b = bytes[idx++];
    if (b == 0x0a) break;
  }

  bool kommentben = false;

  while (idx < bytes.length) {
    int b = bytes[idx++];

    if (b == 0x3e) {
      kommentben = true;
      continue;
    }

    if (b == 0x0a) {
      kommentben = false;
      continue;
    }

    if (kommentben) continue;

    if (b == 0x4e) continue;

    for (int i = 0; i < 8; i++) {
      if ((b & 0x80) != 0) {
        binFa.addBit('1');
      } else {
        binFa.addBit('0');
      }
      b = (b << 1) & 0xFF;
    }
  }

  File kiFile = File(outFile);
  IOSink os = kiFile.openWrite();

  binFa.kiir(os);
  os.write("depth = ${binFa.getMelyseg()}\n");
  os.write("mean = ${binFa.getAtlag()}\n");
  os.write("var = ${binFa.getSzoras()}\n");

  await os.close();
}
