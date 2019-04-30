#include <xinu.h>
#include <actuator.h>
gid8 actuator_gid;
uint32 actuator_pin;

void actuator_initialize(gid8 gid, uint32 pin) {
	actuator_gid = gid;
	actuator_pin = pin;
	gpio_pin_output_pin(gid, pin);
}

uint8 actuator_set(uint32 value) {
	return gpio_write_pin(actuator_gid, actuator_pin, value);
}


