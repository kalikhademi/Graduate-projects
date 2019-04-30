#ifndef DDL_GENERATOR_H_
#define DDL_GENERATOR_H_

#include <vector>
#include <string>
#include <unordered_map>
#include "tinyxml2.h"

class Generator {
public:
  virtual bool generateHeaderFile() = 0;
  virtual bool generateSourceFile() = 0;
};

class SpecifiedGenerator : public Generator {
  std::string device_name;
  std::string headerFile;
  std::string sourceFile;
public:
  SpecifiedGenerator(std::string name, std::string header, std::string source) {
    device_name = name;
    headerFile = header;
    sourceFile = source;
  }
  bool generateHeaderFile();
  bool generateSourceFile();
};

class GenericAnalogGenerator : public Generator {
  std::string device_name;
  std::vector<int> default_pins;
  std::unordered_map<std::string,std::string> measurements;
public:
  GenericAnalogGenerator(std::string name, int pins) {
    for (int i = 0; i < pins; i++)
      default_pins.push_back(-1);
    device_name = name;
  }
  void setDefaultPin(int,int);
  bool hasDefaultPins();
  bool addMeasurement(std::string,std::string);

  bool generateHeaderFile();
  bool generateSourceFile();
};

#endif
