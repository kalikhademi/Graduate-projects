#include <iostream>
#include "tinyxml2.h"
#include "generator.h"
#include "parser.h"

using namespace std;
using namespace tinyxml2;

int main(int argc, char* argv[]) {
  if (argc != 2) {
    cerr << "Parser Error: not enough arguments supplied.\n"
      << "Usage:\n"
      << "\t" << argv[0] << " <DDL>" << endl;
    return 1;
  }

  XMLDocument doc;
  doc.LoadFile(argv[1]);

  if (doc.Error()) {
    cerr << "Parser Error: unable to parse DDL file: " << argv[1] << "\n"
      << "\t" << doc.GetErrorStr1() << endl;
    return 1;
  }

  Parser parser(doc.RootElement());
  Generator *generator = parser.parse();

  if (generator == NULL) {
    cerr << "Malformed DDL file: " << argv[1] << endl;
    return 1;
  }

  if (! generator->generateHeaderFile() ||
      ! generator->generateSourceFile()) {
    return 1;
  }

  return 0;
}
