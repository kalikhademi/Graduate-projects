#ifndef GPIO_H_
#define GPIO_H_

#define GPIO0_ADDR 0x44E07000
#define GPIO1_ADDR 0x4804C000
#define GPIO2_ADDR 0x481AC000
#define GPIO3_ADDR 0x481AE000

struct gpioregister {
  uint32 revision;            // 0x000-0x003
  char padding_0[0xC];        // 0x004-0x009
  uint32 sysconfig;           // 0x010-0x013
  char padding_1[0xC];        // 0x014-0x019
  uint32 eoi;                 // 0x020-0x023
  uint32 irqstatus_raw_0;     // 0x024-0x027
  uint32 irqstatus_raw_1;     // 0x028-0x02B
  uint32 irqstatus_0;         // 0x02C-0x02F
  uint32 irqstatus_1;         // 0x030-0x033
  uint32 irqstatus_set_0;     // 0x034-0x037
  uint32 irqstatus_set_1;     // 0x038-0x03B
  uint32 irqstatus_clr_0;     // 0x03C-0x03F
  uint32 irqstatus_clr_1;     // 0x040-0x043
  uint32 irqwaken_0;          // 0x044-0x047
  uint32 irqwaken_1;          // 0x048-0x04B
  char padding_2[0xC8];       // 0x04C-0x113
  uint32 sysstatus;           // 0x114-0x117
  char padding_3[0x18];       // 0x118-0x129
  uint32 ctrl;                // 0x130-0x133
  uint32 oe;                  // 0x134-0x137
  uint32 datain;              // 0x138-0x13B
  uint32 dataout;             // 0x13C-0x13F
  uint32 leveldetect0;        // 0x140-0x143
  uint32 leveldetect1;        // 0x144-0x147
  uint32 risingdetect;        // 0x148-0x14B
  uint32 fallingdetect;       // 0x14C-0x14F
  uint32 debounceenable;      // 0x150-0x153
  uint32 debouncingtime;      // 0x154-0x157
  char padding_4[0x38];       // 0x158-0x18F
  uint32 cleardataout;        // 0x190-0x193
  uint32 setdataout;          // 0x194-0x197
};

typedef uint8 gpioid8;

struct gpioregister* get_gpio(gpioid8 gid);

void gpio_autoidle_enable(gpioid8 gid);
void gpio_autoidle_disable(gpioid8 gid);
uint32 gpio_autoidle(gpioid8 gid);
void gpio_softreset(gpioid8 gid);
void gpio_wakeup_enable(gpioid8 gid);
void gpio_wakeup_disable(gpioid8 gid);
uint32 gpio_wakeup(gpioid8 gid);
#define GPIO_IDLEMODE_FORCEIDLE 0x0
#define GPIO_IDLEMODE_NOIDLE 0x1
#define GPIO_IDLEMODE_SMARTIDLE 0x2
#define GPIO_IDLEMODE_IDLEWAKEUP 0x3
void gpio_idlemode_write(gpioid8 gid, uint32 value);
uint32 gpio_idlemode(gpioid8 gid);
void gpio_dmaevent_ack(gpioid8 gid);
void gpio_irq0_trigger(gpioid8 gid, uint32 offset, uint32 len, uint32 value);
void gpio_irq0_trigger_pin(gpioid8 gid, uint32 offset, uint32 value);
void gpio_irq0_trigger_all(gpioid8 gid, uint32 value);
void gpio_irq1_trigger(gpioid8 gid, uint32 offset, uint32 len, uint32 value);
void gpio_irq1_trigger_pin(gpioid8 gid, uint32 offset, uint32 value);
void gpio_irq1_trigger_all(gpioid8 gid, uint32 value);
uint32 gpio_irq0_status(gpioid8 gid, uint32 offset, uint32 len);
uint32 gpio_irq0_status_pin(gpioid8 gid, uint32 offset);
uint32 gpio_irq0_status_all(gpioid8 gid);
uint32 gpio_irq1_status(gpioid8 gid, uint32 offset, uint32 len);
uint32 gpio_irq1_status_pin(gpioid8 gid, uint32 offset);
uint32 gpio_irq1_status_all(gpioid8 gid);
void gpio_irq0_clear(gpioid8 gid, uint32 offset, uint32 len, uint32 value);
void gpio_irq0_clear_pin(gpioid8 gid, uint32 offset, uint32 value);
void gpio_irq0_clear_all(gpioid8 gid, uint32 value);
void gpio_irq1_clear(gpioid8 gid, uint32 offset, uint32 len, uint32 value);
void gpio_irq1_clear_pin(gpioid8 gid, uint32 offset, uint32 value);
void gpio_irq1_clear_all(gpioid8 gid, uint32 value);
void gpio_irq0_enable(gpioid8 gid, uint32 offset, uint32 len, uint32 value);
void gpio_irq0_enable_pin(gpioid8 gid, uint32 offset, uint32 value);
void gpio_irq0_enable_all(gpioid8 gid, uint32 value);
void gpio_irq1_enable(gpioid8 gid, uint32 offset, uint32 len, uint32 value);
void gpio_irq1_enable_pin(gpioid8 gid, uint32 offset, uint32 value);
void gpio_irq1_enable_all(gpioid8 gid, uint32 value);
void gpio_irq0_disable(gpioid8 gid, uint32 offset, uint32 len, uint32 value);
void gpio_irq0_disable_pin(gpioid8 gid, uint32 offset, uint32 value);
void gpio_irq0_disable_all(gpioid8 gid, uint32 value);
void gpio_irq1_disable(gpioid8 gid, uint32 offset, uint32 len, uint32 value);
void gpio_irq1_disable_pin(gpioid8 gid, uint32 offset, uint32 value);
void gpio_irq1_disable_all(gpioid8 gid, uint32 value);
uint32 gpio_resetdone(gpioid8 gid);
void gpio_module_enable(gpioid8 gid);
void gpio_module_disable(gpioid8 gid);
uint32 gpio_module(gpioid8 gid);
void gpio_gatingratio_write(gpioid8 gid, uint32 value);
uint32 gpio_gatingratio(gpioid8 gid);
void gpio_pin_output(gpioid8 gid, uint32 offset, uint32 len);
void gpio_pin_output_pin(gpioid8 gid, uint32 offset);
void gpio_pin_output_all(gpioid8 gid);
void gpio_pin_input(gpioid8 gid, uint32 offset, uint32 len);
void gpio_pin_input_pin(gpioid8 gid, uint32 offset);
void gpio_pin_input_all(gpioid8 gid);
uint32 gpio_pin(gpioid8 gid, uint32 offset, uint32 len);
uint32 gpio_pin_pin(gpioid8 gid, uint32 offset);
uint32 gpio_pin_all(gpioid8 gid);
uint32 gpio_read(gpioid8 gid, uint32 offset, uint32 len);
uint32 gpio_read_pin(gpioid8 gid, uint32 offset);
uint32 gpio_read_all(gpioid8 gid);
void gpio_write(gpioid8 gid, uint32 offset, uint32 len, uint32 value);
void gpio_write_pin(gpioid8 gid, uint32 offset, uint32 value);
void gpio_write_all(gpioid8 gid, uint32 value);
void gpio_irq_lowlevel_enable(gpioid8 gid, uint32 offset, uint32 len);
void gpio_irq_lowlevel_enable_pin(gpioid8 gid, uint32 offset);
void gpio_irq_lowlevel_enable_all(gpioid8 gid);
void gpio_irq_lowlevel_disable(gpioid8 gid, uint32 offset, uint32 len);
void gpio_irq_lowlevel_disable_pin(gpioid8 gid, uint32 offset);
void gpio_irq_lowlevel_disable_all(gpioid8 gid);
uint32 gpio_irq_lowlevel(gpioid8 gid, uint32 offset, uint32 len);
uint32 gpio_irq_lowlevel_pin(gpioid8 gid, uint32 offset);
uint32 gpio_irq_lowlevel_all(gpioid8 gid);
void gpio_irq_highlevel_enable(gpioid8 gid, uint32 offset, uint32 len);
void gpio_irq_highlevel_enable_pin(gpioid8 gid, uint32 offset);
void gpio_irq_highlevel_enable_all(gpioid8 gid);
void gpio_irq_highlevel_disable(gpioid8 gid, uint32 offset, uint32 len);
void gpio_irq_highlevel_disable_pin(gpioid8 gid, uint32 offset);
void gpio_irq_highlevel_disable_all(gpioid8 gid);
uint32 gpio_irq_highlevel(gpioid8 gid, uint32 offset, uint32 len);
uint32 gpio_irq_highlevel_pin(gpioid8 gid, uint32 offset);
uint32 gpio_irq_highlevel_all(gpioid8 gid);
void gpio_irq_rising_enable(gpioid8 gid, uint32 offset, uint32 len);
void gpio_irq_rising_enable_pin(gpioid8 gid, uint32 offset);
void gpio_irq_rising_enable_all(gpioid8 gid);
void gpio_irq_rising_disable(gpioid8 gid, uint32 offset, uint32 len);
void gpio_irq_rising_disable_pin(gpioid8 gid, uint32 offset);
void gpio_irq_rising_disable_all(gpioid8 gid);
uint32 gpio_irq_rising(gpioid8 gid, uint32 offset, uint32 len);
uint32 gpio_irq_rising_pin(gpioid8 gid, uint32 offset);
uint32 gpio_irq_rising_all(gpioid8 gid);
void gpio_irq_falling_enable(gpioid8 gid, uint32 offset, uint32 len);
void gpio_irq_falling_enable_pin(gpioid8 gid, uint32 offset);
void gpio_irq_falling_enable_all(gpioid8 gid);
void gpio_irq_falling_disable(gpioid8 gid, uint32 offset, uint32 len);
void gpio_irq_falling_disable_pin(gpioid8 gid, uint32 offset);
void gpio_irq_falling_disable_all(gpioid8 gid);
uint32 gpio_irq_falling(gpioid8 gid, uint32 offset, uint32 len);
uint32 gpio_irq_falling_pin(gpioid8 gid, uint32 offset);
uint32 gpio_irq_falling_all(gpioid8 gid);

//TODO: irqwaken

//TODO: debounceenable

//TODO: debouncingtime

//TODO: cleardataout

//TODO: setdataout

#endif
