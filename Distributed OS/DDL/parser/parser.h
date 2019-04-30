#ifndef DDL_PARSER_H_
#define DDL_PARSER_H_
#include <string>
#include "tinyxml2.h"
#include "generator.h"

class Parser {
  tinyxml2::XMLElement* root;
  std::string trim(std::string);
  Generator* parseSpecified();
  Generator* parseGeneric();
  Generator* parseDigitalGeneric();
  Generator* parseAnalogGeneric();
public:
  Parser(tinyxml2::XMLElement* root) : root(root) {}
  Generator* parse();
};

#endif
