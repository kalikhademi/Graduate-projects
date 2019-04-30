
#include <xinu.h>
#include <temperature_sensor.h>

uint32 temperature_sensor_pins[1];
uint32 temperature_sensor_pin_values[1];
uint32 temperature_sensor_dirty_pins;
void (*temperature_sensor_supplied_callback)(uint32);

void temperature_sensor_set_pin(uint32 pin_id, uint32 pin_number) {
  temperature_sensor_pins[pin_id] = pin_number;
}

void temperature_sensor_initialize(void) {
 temperature_sensor_pins[0] = 0;
 temperature_sensor_supplied_callback = NULL;
}


uint32 temperature_sensor_get_temprature_centigrade_blocking(void) {
  uint32 i;
  uint32 mask = 0
   | (1 << 0)
;
  adc_invalidate_blocking(mask);
  for (i = 0; i < 1; i++) {
    temperature_sensor_pin_values[i] = 
      adc_value(temperature_sensor_pins[i]);
  }
  uint32* P = temperature_sensor_pin_values;
  return 10*P[0] - 5000;
}

void temperature_sensor_callback_temprature_centigrade(uint32 pin_number, uint32 pin_value) {
  temperature_sensor_pin_values[pin_number] = pin_value;
  temperature_sensor_dirty_pins--;
  if (temperature_sensor_dirty_pins == 0) {
    uint32* P = temperature_sensor_pin_values;
    if (temperature_sensor_supplied_callback) {
      temperature_sensor_supplied_callback(10*P[0] - 5000);
      temperature_sensor_supplied_callback = NULL;
    }
  }
}

void temperature_sensor_get_temprature_centigrade_callback(void(*clbk)(uint32)) {
  temperature_sensor_supplied_callback = clbk;
  uint32 mask = 0
   | (1 << 0)
;
  temperature_sensor_dirty_pins = 1;
  adc_invalidate_callback(mask, temperature_sensor_callback_temprature_centigrade);
}
