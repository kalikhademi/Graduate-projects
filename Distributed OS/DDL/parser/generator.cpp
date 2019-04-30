#include "generator.h"
#include <iostream>
#include <fstream>

using namespace tinyxml2;
using namespace std;

bool SpecifiedGenerator::generateHeaderFile() {
  ifstream fin(headerFile.c_str(), ios::binary);
  string filename = "include/" + device_name + ".h";
  ofstream fout(filename.c_str(), ios::binary);
  if (! fin.is_open()) {
    cerr << "Cannot open given header file: " << headerFile << endl;
    return false;
  }
  if (! fout.is_open()) {
    cerr << "Cannot write to " << filename << endl;
    return false;
  }

  fout << fin.rdbuf();

  fin.close();
  fout.close();
  return true;
}

bool SpecifiedGenerator::generateSourceFile() {
  ifstream fin(sourceFile.c_str(), ios::binary);
  string filename = "impl/" + device_name + ".c";
  ofstream fout(filename.c_str(), ios::binary);
  if (! fin.is_open()) {
    cerr << "Cannot open given source file: " << sourceFile << endl;
    return false;
  }
  if (! fout.is_open()) {
    cerr << "Cannot write to " << filename << endl;
    return false;
  }

  fout << fin.rdbuf();

  fin.close();
  fout.close();
  return true;
}

void GenericAnalogGenerator::setDefaultPin(int pin_id, int pin_number) {
  default_pins[pin_id] = pin_number;
}

bool GenericAnalogGenerator::hasDefaultPins() {
  for (int i = 0; i < default_pins.size(); i++)
    if (default_pins[i] == -1) return false;
  return true;
}

bool GenericAnalogGenerator::addMeasurement(string name, string expression) {
  if (measurements.find(name) != measurements.end()) return false;
  measurements[name] = expression;
  return true;
}


bool GenericAnalogGenerator::generateHeaderFile() {
  string filename = "include/" + device_name + ".h";
  ofstream fout(filename.c_str());
  if (! fout.is_open()) {
    cerr << "Cannot write to " << filename << endl;
    return false;
  }
  fout << R"(
/************************************
 * THIS FILE CONTAIN GENERATED CODE *
 *           DO NOT EDIT!           *
 * **********************************/
#ifndef DEVICE_GENERATED_CODE_)" << device_name << R"(_H_
#define DEVICE_GENERATED_CODE_)" << device_name << R"(_H_
#include <xinu.h>

extern void )" << device_name << R"(_set_pin(uint32, uint32);
extern void )" << device_name << R"(_initialize(void);
)";

  for (auto p : measurements) {
    fout << R"(
extern uint32 )" << device_name << R"(_get_)" << p.first << R"(_blocking(void);
extern void )" << device_name << R"(_get_)" << p.first << R"(_callback(void(*)(uint32));
)";
  }

  fout << R"(

#endif
)";

  fout.close();
  return true;
}
  
bool GenericAnalogGenerator::generateSourceFile() {
  string filename = "impl/" + device_name + ".c";
  ofstream fout(filename.c_str());
  if (! fout.is_open()) {
    cerr << "Cannot write to " << filename << endl;
    return false;
  }
  fout << R"(
#include <xinu.h>
#include <)" << device_name << R"(.h>

uint32 )" << device_name << R"(_pins[)" << default_pins.size() << R"(];
uint32 )" << device_name << R"(_pin_values[)" << default_pins.size() << R"(];
uint32 )" << device_name << R"(_dirty_pins;
void (*)" << device_name << R"(_supplied_callback)(uint32);

void )" << device_name << R"(_set_pin(uint32 pin_id, uint32 pin_number) {
  )" << device_name << R"(_pins[pin_id] = pin_number;
}

void )" << device_name << R"(_initialize(void) {
)";

  for (int i = 0; i < default_pins.size(); i++) {
    fout << R"( )" << device_name << R"(_pins[)" << i << R"(] = )" << default_pins[i] << R"(;
)";
  }
  fout << R"( )" << device_name << R"(_supplied_callback = NULL;
}

)";

  for (auto p : measurements) {
    fout << R"(
uint32 )" << device_name << R"(_get_)" << p.first << R"(_blocking(void) {
  uint32 i;
  uint32 mask = 0
)";
    for (int i = 0; i < default_pins.size(); i++) {
      fout << R"(   | (1 << )" << default_pins[i] << R"()
)";
    }
    fout << R"(;
  adc_invalidate_blocking(mask);
  for (i = 0; i < )" << default_pins.size() << R"(; i++) {
    )" << device_name << R"(_pin_values[i] = 
      adc_value()" << device_name << R"(_pins[i]);
  }
  uint32* P = )" << device_name << R"(_pin_values;
  return )" << p.second << R"(;
}

void )" << device_name << R"(_callback_)" << p.first << R"((uint32 pin_number, uint32 pin_value) {
  )" << device_name << R"(_pin_values[pin_number] = pin_value;
  )" << device_name << R"(_dirty_pins--;
  if ()" << device_name << R"(_dirty_pins == 0) {
    uint32* P = )" << device_name << R"(_pin_values;
    if ()" << device_name << R"(_supplied_callback) {
      )" << device_name << R"(_supplied_callback()" << p.second << R"();
      )" << device_name << R"(_supplied_callback = NULL;
    }
  }
}

void )" << device_name << R"(_get_)" << p.first << R"(_callback(void(*clbk)(uint32)) {
  )" << device_name << R"(_supplied_callback = clbk;
  uint32 mask = 0
)";
    for (int i = 0; i < default_pins.size(); i++) {
      fout << R"(   | (1 << )" << default_pins[i] << R"()
)";
    }
    fout << R"(;
  )" << device_name << R"(_dirty_pins = )" << default_pins.size() << R"(;
  adc_invalidate_callback(mask, )" << device_name << R"(_callback_)" << p.first << R"();
}
)";
  }
  
  fout.close();
  return true;
}
