#include "parser.h"
#include <iostream>
#include <algorithm>

using namespace tinyxml2;
using namespace std;

string Parser::trim(string str) {
  int ind;
  for (ind = 0; ind < str.size(); ind++) {
    char c = str[ind];
    if (c  != ' ' && c != '\t' && c != '\n' && c != '\r') break;
  }
  str = str.substr(ind);
  for (ind = str.size()-1; ind >= 0; ind--) {
    char c = str[ind];
    if (c != ' ' && c != '\t' && c != '\n' && c != '\r') break;
  }
  return str.substr(0, ind+1);
}


Generator* Parser::parse() {
  if (root == NULL) return NULL;
  if (root->Attribute("type", "specified"))
    return parseSpecified();
  if (root->Attribute("type", "generic"))
    return parseGeneric();
  return NULL;
}

Generator* Parser::parseSpecified() {
  XMLElement *metadata = root->FirstChildElement("metadata");
  if (metadata == NULL) {
    cerr << "<metadata> not found." << endl;
    return NULL;
  }
  XMLElement *device_name = metadata->FirstChildElement("name");
  if (device_name == NULL) {
    cerr << "<name> not found." << endl;
    return NULL;
  }
  string name = trim(device_name->GetText());
  if (name.size() == 0) {
    cerr << "<name> cannot be empty." << endl;
    return NULL;
  }
  for (int i = 0; i < name.size(); i++) {
    if (name[i] >= 'a' && name[i] <= 'z') continue;
    if (name[i] >= 'A' && name[i] <= 'Z') continue;
    if (i > 0 && name[i] >= '0' && name[i] <= '9') continue;
    if (i > 0 && name[i] == '_') continue;
    cerr << "<name> should contain alphanumeric and underscores "
      "and start with an alphabetical character." << endl;
    return NULL;
  }
  XMLElement *header = root->FirstChildElement("header");
  if (header == NULL) {
    cerr << "<header> not found." << endl;
    return NULL;
  }
  string header_path = trim(header->GetText());
  if (header_path.size() == 0) {
    cerr << "<header> cannot be empty." << endl;
    return NULL;
  }
  XMLElement *source = root->FirstChildElement("source");
  if (source == NULL) {
    cerr << "<source> not found." << endl;
    return NULL;
  }
  string source_path = trim(source->GetText());
  if (source_path.size() == 0) {
    cerr << "<source> cannot be empty." << endl;
    return NULL;
  }
  return new SpecifiedGenerator(name, header_path, source_path);
}

Generator* Parser::parseGeneric() {
  if (root->Attribute("connection", "digital"))
    return parseDigitalGeneric();
  if (root->Attribute("connection", "analog"))
    return parseAnalogGeneric();
  return NULL;
}

Generator* Parser::parseDigitalGeneric() {
  cerr << "Unsupported Type." << endl;
  return NULL;
}

Generator* Parser::parseAnalogGeneric() {
  XMLElement* metadata = root->FirstChildElement("metadata");
  if (metadata == NULL) {
    cerr << "<metadata> not found." << endl;
    return NULL;
  }
  XMLElement* device_name = metadata->FirstChildElement("name");
  if (device_name == NULL) {
    cerr << "<name> not found." << endl;
    return NULL;
  }
  string name = trim(device_name->GetText());
  if (name.size() == 0) {
    cerr << "<name> cannot be empty." << endl;
    return NULL;
  }
  for (int i = 0; i < name.size(); i++) {
    if (name[i] >= 'a' && name[i] <= 'z') continue;
    if (name[i] >= 'A' && name[i] <= 'Z') continue;
    if (i > 0 && name[i] >= '0' && name[i] <= '9') continue;
    if (i > 0 && name[i] == '_') continue;
    cerr << "<name> should contain alphanumeric and underscores "
      "and start with an alphabetical character." << endl;
    return NULL;
  }
  XMLElement* def_pins = metadata->FirstChildElement("default_pins");
  if (def_pins == NULL) {
    cerr << "<default_pins> not found." << endl;
    return NULL;
  }
  int pins = def_pins->IntAttribute("number");
  if (pins <= 0 || pins > 8) {
    cerr << "<default_pins>: incorrect value for number." << endl;
    return NULL;
  }
  GenericAnalogGenerator* generator = new GenericAnalogGenerator(name, pins);
  XMLElement* pin_spec = def_pins->FirstChildElement("pin");
  while(pin_spec) {
    int pin_id, pin_number;
    if (pin_spec->QueryIntAttribute("id", &pin_id)) {
      cerr << "<pin>: missing or malformed id attribute." << endl;
      delete generator;
      return NULL;
    }
    if (pin_spec->QueryIntText(&pin_number)) {
      cerr << "<pin>: should contain the pin number." << endl;
      delete generator;
      return NULL;
    }
    if (pin_id < 0 || pin_id >= pins
        || pin_number < 0 || pin_number > 7) {
      cerr << "<pin>: incorrect id or pin number." << endl;
      delete generator;
      return NULL;
    }
    generator->setDefaultPin(pin_id, pin_number);
    pin_spec = pin_spec->NextSiblingElement("pin");
  }
  if ( ! generator->hasDefaultPins()) {
    cerr << "<default_pins>: unspecified default pins." << endl;
    delete generator;
    return NULL;
  }

  XMLElement* measurements = root->FirstChildElement("measurements");
  if (measurements == NULL) {
    cerr << "<measurements> not found." << endl;
    delete generator;
    return NULL;
  }

  XMLElement* measurement = measurements->FirstChildElement("measurement");
  while(measurement) {
    if ( ! measurement->Attribute("name")) {
      cerr << "<measurement>: missing name attribute." << endl;
      delete generator;
      return NULL;
    }
    string name = measurement->Attribute("name");
    if (name.size() == 0) {
      cerr << "<measurement>: name should not be empty." << endl;
      delete generator;
      return NULL;
    }
    for (int i =0; i < name.size(); i++) {
      if (name[i] >= 'a' && name[i] <= 'z') continue;
      if (name[i] >= 'A' && name[i] <= 'Z') continue;
      if (name[i] == '_') continue;
      cerr << "<measurement>: name should only contain alphabetical characters or underscores."
        << endl;
      delete generator;
      return NULL;
    }
    if ( ! measurement->GetText()) {
      cerr << "<measurement>: should contain an expression." << endl;
      delete generator;
      return NULL;
    }
    string expression = trim(measurement->GetText());
    if (expression.size() == 0) {
      cerr << "<measurement>: expression cannot be empty." << endl;
      delete generator;
      return NULL;
    }
    if ( ! generator->addMeasurement(name, expression)) {
      cerr << "<measurement>: redifinition of " << name << "." << endl;
      delete generator;
      return NULL;
    }
    measurement = measurement->NextSiblingElement("measurement");
  }

  return generator;
}
