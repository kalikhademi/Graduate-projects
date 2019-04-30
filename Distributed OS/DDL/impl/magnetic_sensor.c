#include <xinu.h>
#include <magnetic_sensor.h>
gid8 magnetic_sensor_gid;
uint32 magnetic_sensor_pin;

void magnetic_sensor_initialize(gid8 gid, uint32 pin) {
	magnetic_sensor_gid = gid;
	magnetic_sensor_pin = pin;
	gpio_pin_input_pin(gid, pin);
}

uint8 magnetic_sensor_get() {
	return gpio_read_pin(magnetic_sensor_gid, magnetic_sensor_pin);
}


