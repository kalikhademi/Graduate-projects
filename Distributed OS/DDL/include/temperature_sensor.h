
/************************************
 * THIS FILE CONTAIN GENERATED CODE *
 *           DO NOT EDIT!           *
 * **********************************/
#ifndef DEVICE_GENERATED_CODE_temperature_sensor_H_
#define DEVICE_GENERATED_CODE_temperature_sensor_H_
#include <xinu.h>

extern void temperature_sensor_set_pin(uint32, uint32);
extern void temperature_sensor_initialize(void);

extern uint32 temperature_sensor_get_temprature_centigrade_blocking(void);
extern void temperature_sensor_get_temprature_centigrade_callback(void(*)(uint32));


#endif
