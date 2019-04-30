#include <xinu.h>

struct gpioregister* get_gpio(gpioid8 gid) {
  switch(gid) {
    case 0:
      return ((struct gpioregister*)GPIO0_ADDR);
    case 1:
      return ((struct gpioregister*)GPIO1_ADDR);
    case 2:
      return ((struct gpioregister*)GPIO2_ADDR);
    case 3:
      return ((struct gpioregister*)GPIO3_ADDR);
  }
  return NULL;
}

#define GETREG(gid,name) get_gpio(gid)->name

#define BITWRITE(x,o,l,v) x=((x&(~(((0x1<<l)-1)<<o)))|(v<<o))
#define BITREAD(x,o,l) ((x>>o)&((0x1<<l)-1))
#define BITSET(x,o,l) x|=(((0x1<<l)-1)<<o)
#define BITCLR(x,o,l) x&=~(((0x1<<l)-1)<<o)

#define GENSG(name,reg,o,l) \
void gpio_##name##_write(gpioid8 gid, uint32 value) { \
  BITWRITE(GETREG(gid,reg), o, l, value); \
} \
uint32 gpio_##name(gpioid8 gid) { \
  return BITREAD(GETREG(gid,reg), o, l); \
}

#define GENEDR(name,reg,o) \
void gpio_##name##_enable(gpioid8 gid) { \
  BITSET(GETREG(gid,reg), o, 1); \
} \
void gpio_##name##_disable(gpioid8 gid) { \
  BITCLR(GETREG(gid,reg), o, 1); \
} \
uint32 gpio_##name(gpioid8 gid) { \
  return BITREAD(GETREG(gid, reg), o, 1); \
}

GENEDR(autoidle, sysconfig, 0);

void gpio_softreset(gpioid8 gid) {
  BITSET(GETREG(gid,sysconfig), 1, 1);
}

GENEDR(wakeup, sysconfig, 2);

GENSG(idlemode, sysconfig, 3, 2);

void gpio_dmaevent_ack(gpioid8 gid) {
  BITCLR(GETREG(gid,eoi), 0, 1);
}

void gpio_irq0_trigger(gpioid8 gid, uint32 offset, uint32 len, uint32 value) {
  BITWRITE(GETREG(gid,irqstatus_raw_0), offset, len, value);
}
void gpio_irq0_trigger_pin(gpioid8 gid, uint32 offset, uint32 value) { gpio_irq0_trigger(gid, offset, 1, value); }
void gpio_irq0_trigger_all(gpioid8 gid, uint32 value) { gpio_irq0_trigger(gid, 0, 32, value); }

void gpio_irq1_trigger(gpioid8 gid, uint32 offset, uint32 len, uint32 value) {
  BITWRITE(GETREG(gid,irqstatus_raw_1), offset, len, value);
}
void gpio_irq1_trigger_pin(gpioid8 gid, uint32 offset, uint32 value) { gpio_irq1_trigger(gid, offset, 1, value); }
void gpio_irq1_trigger_all(gpioid8 gid, uint32 value) { gpio_irq1_trigger(gid, 0, 32, value); }

uint32 gpio_irq0_status(gpioid8 gid, uint32 offset, uint32 len) {
  return BITREAD(GETREG(gid,irqstatus_0), offset, len);
}
uint32 gpio_irq0_status_pin(gpioid8 gid, uint32 offset) { return gpio_irq0_status(gid, offset, 1); }
uint32 gpio_irq0_status_all(gpioid8 gid) { return gpio_irq0_status(gid, 0, 32); }

uint32 gpio_irq1_status(gpioid8 gid, uint32 offset, uint32 len) {
  return BITREAD(GETREG(gid,irqstatus_1), offset, len);
}
uint32 gpio_irq1_status_pin(gpioid8 gid, uint32 offset) { return gpio_irq1_status(gid, offset, 1); }
uint32 gpio_irq1_status_all(gpioid8 gid) { return gpio_irq1_status(gid, 0, 32); }

void gpio_irq0_clear(gpioid8 gid, uint32 offset, uint32 len, uint32 value) {
  BITWRITE(GETREG(gid,irqstatus_0), offset, len, value);
}
void gpio_irq0_clear_pin(gpioid8 gid, uint32 offset, uint32 value) { gpio_irq0_clear(gid, offset, 1, value); }
void gpio_irq0_clear_all(gpioid8 gid, uint32 value) { gpio_irq0_clear(gid, 0, 32, value); }

void gpio_irq1_clear(gpioid8 gid, uint32 offset, uint32 len, uint32 value) {
  BITWRITE(GETREG(gid,irqstatus_1), offset, len, value);
}
void gpio_irq1_clear_pin(gpioid8 gid, uint32 offset, uint32 value) { gpio_irq1_clear(gid, offset, 1, value); }
void gpio_irq1_clear_all(gpioid8 gid, uint32 value) { gpio_irq1_clear(gid, 0, 32, value); }

void gpio_irq0_enable(gpioid8 gid, uint32 offset, uint32 len, uint32 value) {
  BITWRITE(GETREG(gid,irqstatus_set_0), offset, len, value);
}
void gpio_irq0_enable_pin(gpioid8 gid, uint32 offset, uint32 value) { gpio_irq0_enable(gid, offset, 1, value); }
void gpio_irq0_enable_all(gpioid8 gid, uint32 value) { gpio_irq0_enable(gid, 0, 32, value); }

void gpio_irq1_enable(gpioid8 gid, uint32 offset, uint32 len, uint32 value) {
  BITWRITE(GETREG(gid,irqstatus_set_1), offset, len, value);
}
void gpio_irq1_enable_pin(gpioid8 gid, uint32 offset, uint32 value) { gpio_irq1_enable(gid, offset, 1, value); }
void gpio_irq1_enable_all(gpioid8 gid, uint32 value) { gpio_irq1_enable(gid, 0, 32, value); }

void gpio_irq0_disable(gpioid8 gid, uint32 offset, uint32 len, uint32 value) {
  BITWRITE(GETREG(gid,irqstatus_clr_0), offset, len, value);
}
void gpio_irq0_disable_pin(gpioid8 gid, uint32 offset, uint32 value) { gpio_irq0_disable(gid, offset, 1, value); }
void gpio_irq0_disable_all(gpioid8 gid, uint32 value) { gpio_irq0_disable(gid, 0, 32, value); }

void gpio_irq1_disable(gpioid8 gid, uint32 offset, uint32 len, uint32 value) {
  BITWRITE(GETREG(gid,irqstatus_clr_1), offset, len, value);
}
void gpio_irq1_disable_pin(gpioid8 gid, uint32 offset, uint32 value) { gpio_irq1_disable(gid, offset, 1, value); }
void gpio_irq1_disable_all(gpioid8 gid, uint32 value) { gpio_irq1_disable(gid, 0, 32, value); }

//TODO: irqwakeup

uint32 gpio_resetdone(gpioid8 gid) {
  return BITREAD(GETREG(gid,sysstatus), 0, 1);
}

void gpio_module_enable(gpioid8 gid) {
  BITCLR(GETREG(gid,ctrl), 0, 1);
}

void gpio_module_disable(gpioid8 gid) {
  BITSET(GETREG(gid,ctrl), 0, 1);
}

uint32 gpio_module(gpioid8 gid) {
  return BITREAD(GETREG(gid,ctrl), 0, 1);
}

GENSG(gatingratio, ctrl, 1, 2);

void gpio_pin_output(gpioid8 gid, uint32 offset, uint32 len) {
  BITCLR(GETREG(gid,oe), offset, len);
}
void gpio_pin_output_pin(gpioid8 gid, uint32 offset) { gpio_pin_output(gid, offset, 1); }
void gpio_pin_output_all(gpioid8 gid) { gpio_pin_output(gid, 0, 32); }

void gpio_pin_input(gpioid8 gid, uint32 offset, uint32 len) {
  BITSET(GETREG(gid,oe), offset, len);
}
void gpio_pin_input_pin(gpioid8 gid, uint32 offset) { gpio_pin_input(gid, offset, 1); }
void gpio_pin_input_all(gpioid8 gid) { gpio_pin_input(gid, 0, 32); }

uint32 gpio_pin(gpioid8 gid, uint32 offset, uint32 len) {
  return BITREAD(GETREG(gid,oe), offset, len);
}
uint32 gpio_pin_pin(gpioid8 gid, uint32 offset) { return gpio_pin(gid, offset, 1); }
uint32 gpio_pin_all(gpioid8 gid) { return gpio_pin(gid, 0, 32); }

uint32 gpio_read(gpioid8 gid, uint32 offset, uint32 len) {
  return BITREAD(GETREG(gid,datain), offset, len);
}
uint32 gpio_read_pin(gpioid8 gid, uint32 offset) { return gpio_read(gid, offset, 1); }
uint32 gpio_read_all(gpioid8 gid) { return gpio_read(gid, 0, 32); }

void gpio_write(gpioid8 gid, uint32 offset, uint32 len, uint32 value) {
  BITWRITE(GETREG(gid,dataout), offset, len, value);
}
void gpio_write_pin(gpioid8 gid, uint32 offset, uint32 value) { gpio_write(gid, offset, 1, value); }
void gpio_write_all(gpioid8 gid, uint32 value) { gpio_write(gid, 0, 32, value); }

void gpio_irq_lowlevel_enable(gpioid8 gid, uint32 offset, uint32 len) {
  BITSET(GETREG(gid,leveldetect0), offset, len);
}
void gpio_irq_lowlevel_enable_pin(gpioid8 gid, uint32 offset) { gpio_irq_lowlevel_enable(gid, offset, 1); }
void gpio_irq_lowlevel_enable_all(gpioid8 gid) { gpio_irq_lowlevel_enable(gid, 0, 32); }

void gpio_irq_lowlevel_disable(gpioid8 gid, uint32 offset, uint32 len) {
  BITCLR(GETREG(gid,leveldetect0), offset, len);
}
void gpio_irq_lowlevel_disable_pin(gpioid8 gid, uint32 offset) { gpio_irq_lowlevel_disable(gid, offset, 1); }
void gpio_irq_lowlevel_disable_all(gpioid8 gid) { gpio_irq_lowlevel_disable(gid, 0, 32); }

uint32 gpio_irq_lowlevel(gpioid8 gid, uint32 offset, uint32 len) {
  return BITREAD(GETREG(gid,leveldetect0), offset, len);
}
uint32 gpio_irq_lowlevel_pin(gpioid8 gid, uint32 offset) { return gpio_irq_lowlevel(gid, offset, 1); }
uint32 gpio_irq_lowlevel_all(gpioid8 gid) { return gpio_irq_lowlevel(gid, 0, 32); }

void gpio_irq_highlevel_enable(gpioid8 gid, uint32 offset, uint32 len) {
  BITSET(GETREG(gid,leveldetect1), offset, len);
}
void gpio_irq_highlevel_enable_pin(gpioid8 gid, uint32 offset) { gpio_irq_highlevel_enable(gid, offset, 1); }
void gpio_irq_highlevel_enable_all(gpioid8 gid) { gpio_irq_highlevel_enable(gid, 0, 32); }

void gpio_irq_highlevel_disable(gpioid8 gid, uint32 offset, uint32 len) {
  BITCLR(GETREG(gid,leveldetect1), offset, len);
}
void gpio_irq_highlevel_disable_pin(gpioid8 gid, uint32 offset) { gpio_irq_highlevel_disable(gid, offset, 1); }
void gpio_irq_highlevel_disable_all(gpioid8 gid) { gpio_irq_highlevel_disable(gid, 0, 32); }

uint32 gpio_irq_highlevel(gpioid8 gid, uint32 offset, uint32 len) {
  return BITREAD(GETREG(gid,leveldetect1), offset, len);
}
uint32 gpio_irq_highlevel_pin(gpioid8 gid, uint32 offset) { return gpio_irq_highlevel(gid, offset, 1); }
uint32 gpio_irq_highlevel_all(gpioid8 gid) { return gpio_irq_highlevel(gid, 0, 32); }

void gpio_irq_rising_enable(gpioid8 gid, uint32 offset, uint32 len) {
  BITSET(GETREG(gid,risingdetect), offset, len);
}
void gpio_irq_rising_enable_pin(gpioid8 gid, uint32 offset) { gpio_irq_rising_enable(gid, offset, 1); }
void gpio_irq_rising_enable_all(gpioid8 gid) { gpio_irq_rising_enable(gid, 0, 32); }

void gpio_irq_rising_disable(gpioid8 gid, uint32 offset, uint32 len) {
  BITCLR(GETREG(gid,risingdetect), offset, len);
}
void gpio_irq_rising_disable_pin(gpioid8 gid, uint32 offset) { gpio_irq_rising_disable(gid, offset, 1); }
void gpio_irq_rising_disable_all(gpioid8 gid) { gpio_irq_rising_disable(gid, 0, 32); }

uint32 gpio_irq_rising(gpioid8 gid, uint32 offset, uint32 len) {
  return BITREAD(GETREG(gid,risingdetect), offset, len);
}
uint32 gpio_irq_rising_pin(gpioid8 gid, uint32 offset) { return gpio_irq_rising(gid, offset, 1); }
uint32 gpio_irq_rising_all(gpioid8 gid) { return gpio_irq_rising(gid, 0, 32); }

void gpio_irq_falling_enable(gpioid8 gid, uint32 offset, uint32 len) {
  BITSET(GETREG(gid,fallingdetect), offset, len);
}
void gpio_irq_falling_enable_pin(gpioid8 gid, uint32 offset) { gpio_irq_falling_enable(gid, offset, 1); }
void gpio_irq_falling_enable_all(gpioid8 gid) { gpio_irq_falling_enable(gid, 0, 32); }

void gpio_irq_falling_disable(gpioid8 gid, uint32 offset, uint32 len) {
  BITCLR(GETREG(gid,fallingdetect), offset, len);
}
void gpio_irq_falling_disable_pin(gpioid8 gid, uint32 offset) { gpio_irq_falling_disable(gid, offset, 1); }
void gpio_irq_falling_disable_all(gpioid8 gid) { gpio_irq_falling_disable(gid, 0, 32); }

uint32 gpio_irq_falling(gpioid8 gid, uint32 offset, uint32 len) {
  return BITREAD(GETREG(gid,fallingdetect), offset, len);
}
uint32 gpio_irq_falling_pin(gpioid8 gid, uint32 offset) { return gpio_irq_falling(gid, offset, 1); }
uint32 gpio_irq_falling_all(gpioid8 gid) { return gpio_irq_falling(gid, 0, 32); }

//TODO: debounceenable

//TODO: debouncingtime

//TODO: cleardataout

//TODO: setdataout
