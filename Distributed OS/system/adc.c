#include <xinu.h>

uint32 adc_ain_val[8];
uint8 adc_ain_dirty[8];
void (*adc_ain_callbacks[8])(uint32, uint32);

volatile struct adcregister *adc_register() {
  return (volatile struct adcregister*) ADC_ADDR;
}

void adc_init(void)
{
  volatile struct adcregister *adc = adc_register();
  int chan;
  uint32 *cm_wkup_adc_tsc_clkctrl;

  kprintf("Starting ADC init\n");

  cm_wkup_adc_tsc_clkctrl = (uint32*)0x44E004BC;
  *cm_wkup_adc_tsc_clkctrl |= 0x2; // enable the clock
  while (!((*cm_wkup_adc_tsc_clkctrl) & 0x2)); // wait for clock to run

  for (chan = 0; chan < 8; chan++) {
    adc_ain_val[chan] = 0;
    adc_ain_dirty[chan] = FALSE;
    adc_ain_callbacks[chan] = NULL;
  }
  
  kprintf("CLK: %x\n", *cm_wkup_adc_tsc_clkctrl);
  kprintf("CLK: %x\n", *cm_wkup_adc_tsc_clkctrl);
  kprintf("CLK: %x\n", *cm_wkup_adc_tsc_clkctrl);
  kprintf("CLK: %x\n", *cm_wkup_adc_tsc_clkctrl);
  kprintf("CLK: %x\n", *cm_wkup_adc_tsc_clkctrl);
  kprintf("CLK: %x\n", *cm_wkup_adc_tsc_clkctrl);
  kprintf("CLK: %x\n", *cm_wkup_adc_tsc_clkctrl);

  adc->ctrl |= 0x6; // enable tag writing and remove config protection

  for (chan = 0; chan < 8; chan++) {
    adc->stepconfigs[chan].config |= (0x1 << 26) | (chan << 19); // one shot in fifo1
  }

  //ADPRINT(adc->fifo1threshold);
  //adc->fifo1threshold = 0x7; // Set fifo threshold to 8

  adc->irqenable_set |= 0x1 << 5; // enable fifo1 threshold intrrupt

  adc->stepenable |= 0x1FE; // enable steps 0b1,1111,1110

  set_evec(ADC_GEN_IRQ, (uint32)adc_handler);

  kprintf("Enabling ADC\n");

  adc->ctrl |= 0x1; // enable adc
  kprintf("Done\n");
}

void adc_handler()
{
  volatile struct adcregister *adc = adc_register();
  uint32 data, pin, value;
  void (*clbk)(uint32, uint32);

  kprintf("Int: %x\n", adc->irqstatus);

  // check for fifo1 thresho int
  if ((adc->irqstatus & 0x20) == 0) return;

  // Ack the int
  adc->irqstatus = 0x20;

  while ((adc->fifo1count & 0x7F) > 0) {
    data = adc->fifo1data;
    pin = (data>>16)&0xF;
    value = data&0xFFF;
    adc_ain_val[pin] = value;
    adc_ain_dirty[pin] = FALSE;
    clbk = adc_ain_callbacks[pin];
    adc_ain_callbacks[pin] = NULL;
    if (clbk) clbk(pin, value);
  }
}

void adc_invalidate(uint32 pin_mask) {
  volatile struct adcregister *adc = adc_register();
  int pin, mask = pin_mask;

  for (pin = 0;mask;mask>>=1,pin++)
    if (mask & 1) adc_ain_dirty[pin] = TRUE;

  adc->stepenable |= pin_mask << 1;
}

void adc_invalidate_blocking(uint32 pin_mask) {
  volatile struct adcregister *adc = adc_register();
  uint32 pin, mask;

  for (pin=0,mask=pin_mask;mask;mask>>=1,pin++)
    if (mask & 1) adc_ain_dirty[pin] = TRUE;

  adc->stepenable |= pin_mask << 1;

  for (pin=0,mask=pin_mask;mask;mask>>=1,pin++)
    if (mask & 1)
      for(;adc_ain_dirty[pin];);
}

void adc_invalidate_callback(uint32 pin_mask, void (*callback)(uint32, uint32)) {
  volatile struct adcregister *adc = adc_register();
  uint32 pin, mask;

  for (pin=0,mask=pin_mask;mask;mask>>=1,pin++)
    if (mask & 1) {
      adc_ain_dirty[pin] = TRUE;
      adc_ain_callbacks[pin] = callback;
    }

  adc->stepenable |= pin_mask << 1;
}

uint8 adc_is_dirty(uint32 pin) {
  return adc_ain_dirty[pin];
}

uint32 adc_value(uint32 pin) {
  return adc_ain_val[pin];
}
