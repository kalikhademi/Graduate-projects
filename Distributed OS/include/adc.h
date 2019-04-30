/* adc.h */

extern uint32 adc_ain_val[8];
extern uint8 adc_ain_dirty[8];
extern void (*adc_ain_callbacks[8])(uint32, uint32);

struct adcregister {
  uint32 revision;  // 0x000 - 0x004
  char padding_1[0xC];  // 0x004 - 0x010
  uint32 sysconfig;  // 0x010 - 0x014
  char padding_2[0x10];  // 0x014 - 0x024
  uint32 irqstatus_raw;  // 0x024 - 0x028
  uint32 irqstatus;  // 0x028 - 0x02C
  uint32 irqenable_set;  // 0x02C - 0x030
  uint32 irqenable_clr;  // 0x030 - 0x034
  uint32 irqwakeup;  // 0x034 - 0x038
  uint32 dmaenable_set;  // 0x038 - 0x03C
  uint32 dmaenable_clr;  // 0x03C - 0x040
  uint32 ctrl;  // 0x040 - 0x044
  uint32 adcstat;  // 0x044 - 0x048
  uint32 adcrange;  // 0x048 - 0x04C
  uint32 adc_clkdiv;  // 0x04C - 0x050
  uint32 adc_misc;  // 0x050 - 0x054
  uint32 stepenable;  // 0x054 - 0x058
  uint32 idleconfig;  // 0x058 - 0x05C
  uint32 ts_charge_stepconfig;  // 0x05C - 0x060
  uint32 ts_charge_delay;  // 0x060 - 0x064
  struct {
    uint32 config;
    uint32 delay;
  } stepconfigs[16];  // 0x064 - 0x0E4
  uint32 fifo0count;  // 0x0E4 - 0x0E8
  uint32 fifo0threshold;  // 0x0E8 - 0x0EC
  uint32 dma0req;  // 0x0EC - 0x0F0
  uint32 fifo1count;  // 0x0F0 - 0x0F4
  uint32 fifo1threshold;  // 0x0F4 - 0x0F8
  uint32 dma1req;  // 0x0F8 - 0x0FC
  char padding_3[0x4];  // 0x0FC - 0x100
  uint32 fifo0data; // 0x100 - 0x104
  char padding_4[0xFC]; // 0x104 - 0x200
  uint32 fifo1data; // 0x200 - 0x204
};

#define ADC_ADDR 0x44E0D000
#define ADC_GEN_IRQ 16

extern void adc_init(void);
extern interrupt adc_handler(void);

extern void adc_invalidate(uint32);
extern void adc_invalidate_blocking(uint32);
extern void adc_invalidate_callback(uint32, void(*)(uint32, uint32));

extern uint8 adc_is_valid(uint32);
extern uint32 adc_value(uint32);
