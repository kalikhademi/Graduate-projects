/* xsh_gpiocli.c - xsh_gpiocli */

#include <xinu.h>
#include <string.h>
#include <stdio.h>

static void nargs_error(char* name, int expected);
static uint32 parse_num(char* string);
static void gid_error(gpioid8 gid);
static void print_res(uint32 res);

/*------------------------------------------------------------------------
 * xsh_gpiocli - direct access to low level gpio calls
 *------------------------------------------------------------------------
 */
shellcmd xsh_gpiocli(int nargs, char *args[])
{
  char *name;

	/* For argument '--help', emit help about the 'memdump' command	*/

	if (nargs == 2 && strncmp(args[1], "--help", 7) == 0) {
    printf("Use: %s function args...\n\n", args[0]);
		printf("Description:\n");
    printf("\tGives direct access to the gpio low level\n");
    printf("\tfunction calls.\n");
		printf("Options:\n");
		printf("\tfunction   name of the function to be called\n");
		printf("\targs...    function arguments separated by space\n");
		return 0;
	}

	/* Check for valid number of arguments */

	if (nargs < 3) {
		fprintf(stderr, "%s: incorrect number of arguments\n",
				args[0]);
		fprintf(stderr, "Try '%s --help' for more information\n",
				args[0]);
		return 1;
	}

  name = args[1];
  if (strncmp(name, "gpio_autoidle_enable",21) == 0) {
    if (nargs != 3) {
      nargs_error(name,3);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    gpio_autoidle_enable(gid);
  }
  else if (strncmp(name, "gpio_autoidle_disable",22) == 0) {
    if (nargs != 3) {
      nargs_error(name,3);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    gpio_autoidle_disable(gid);
  }
  else if (strncmp(name, "gpio_autoidle",14) == 0) {
    if (nargs != 3) {
      nargs_error(name,3);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    print_res(gpio_autoidle(gid));
  }
  else if (strncmp(name, "gpio_softreset",15) == 0) {
    if (nargs != 3) {
      nargs_error(name,3);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    gpio_softreset(gid);
  }
  else if (strncmp(name, "gpio_wakeup_enable",19) == 0) {
    if (nargs != 3) {
      nargs_error(name,3);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    gpio_wakeup_enable(gid);
  }
  else if (strncmp(name, "gpio_wakeup_disable",20) == 0) {
    if (nargs != 3) {
      nargs_error(name,3);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    gpio_wakeup_disable(gid);
  }
  else if (strncmp(name, "gpio_wakeup",12) == 0) {
    if (nargs != 3) {
      nargs_error(name,3);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    print_res(gpio_wakeup(gid));
  }
  else if (strncmp(name, "gpio_idlemode_write",20) == 0) {
    if (nargs != 4) {
      nargs_error(name,4);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    gpio_idlemode_write(gid,val1);
  }
  else if (strncmp(name, "gpio_idlemode",14) == 0) {
    if (nargs != 3) {
      nargs_error(name,3);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    print_res(gpio_idlemode(gid));
  }
  else if (strncmp(name, "gpio_dmaevent_ack",18) == 0) {
    if (nargs != 3) {
      nargs_error(name,3);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    gpio_dmaevent_ack(gid);
  }
  else if (strncmp(name, "gpio_irq0_trigger",18) == 0) {
    if (nargs != 6) {
      nargs_error(name,6);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    uint32 val2 = parse_num(args[4]);
    uint32 val3 = parse_num(args[5]);
    gpio_irq0_trigger(gid,val1,val2,val3);
  }
  else if (strncmp(name, "gpio_irq0_trigger_pin",22) == 0) {
    if (nargs != 5) {
      nargs_error(name,5);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    uint32 val2 = parse_num(args[4]);
    gpio_irq0_trigger_pin(gid,val1,val2);
  }
  else if (strncmp(name, "gpio_irq0_trigger_all",22) == 0) {
    if (nargs != 4) {
      nargs_error(name,4);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    gpio_irq0_trigger_all(gid,val1);
  }
  else if (strncmp(name, "gpio_irq1_trigger",18) == 0) {
    if (nargs != 6) {
      nargs_error(name,6);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    uint32 val2 = parse_num(args[4]);
    uint32 val3 = parse_num(args[5]);
    gpio_irq1_trigger(gid,val1,val2,val3);
  }
  else if (strncmp(name, "gpio_irq1_trigger_pin",22) == 0) {
    if (nargs != 5) {
      nargs_error(name,5);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    uint32 val2 = parse_num(args[4]);
    gpio_irq1_trigger_pin(gid,val1,val2);
  }
  else if (strncmp(name, "gpio_irq1_trigger_all",22) == 0) {
    if (nargs != 4) {
      nargs_error(name,4);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    gpio_irq1_trigger_all(gid,val1);
  }
  else if (strncmp(name, "gpio_irq0_status",17) == 0) {
    if (nargs != 5) {
      nargs_error(name,5);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    uint32 val2 = parse_num(args[4]);
    print_res(gpio_irq0_status(gid,val1,val2));
  }
  else if (strncmp(name, "gpio_irq0_status_pin",21) == 0) {
    if (nargs != 4) {
      nargs_error(name,4);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    print_res(gpio_irq0_status_pin(gid,val1));
  }
  else if (strncmp(name, "gpio_irq0_status_all",21) == 0) {
    if (nargs != 3) {
      nargs_error(name,3);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    print_res(gpio_irq0_status_all(gid));
  }
  else if (strncmp(name, "gpio_irq1_status",17) == 0) {
    if (nargs != 5) {
      nargs_error(name,5);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    uint32 val2 = parse_num(args[4]);
    print_res(gpio_irq1_status(gid,val1,val2));
  }
  else if (strncmp(name, "gpio_irq1_status_pin",21) == 0) {
    if (nargs != 4) {
      nargs_error(name,4);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    print_res(gpio_irq1_status_pin(gid,val1));
  }
  else if (strncmp(name, "gpio_irq1_status_all",21) == 0) {
    if (nargs != 3) {
      nargs_error(name,3);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    print_res(gpio_irq1_status_all(gid));
  }
  else if (strncmp(name, "gpio_irq0_clear",16) == 0) {
    if (nargs != 6) {
      nargs_error(name,6);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    uint32 val2 = parse_num(args[4]);
    uint32 val3 = parse_num(args[5]);
    gpio_irq0_clear(gid,val1,val2,val3);
  }
  else if (strncmp(name, "gpio_irq0_clear_pin",20) == 0) {
    if (nargs != 5) {
      nargs_error(name,5);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    uint32 val2 = parse_num(args[4]);
    gpio_irq0_clear_pin(gid,val1,val2);
  }
  else if (strncmp(name, "gpio_irq0_clear_all",20) == 0) {
    if (nargs != 4) {
      nargs_error(name,4);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    gpio_irq0_clear_all(gid,val1);
  }
  else if (strncmp(name, "gpio_irq1_clear",16) == 0) {
    if (nargs != 6) {
      nargs_error(name,6);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    uint32 val2 = parse_num(args[4]);
    uint32 val3 = parse_num(args[5]);
    gpio_irq1_clear(gid,val1,val2,val3);
  }
  else if (strncmp(name, "gpio_irq1_clear_pin",20) == 0) {
    if (nargs != 5) {
      nargs_error(name,5);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    uint32 val2 = parse_num(args[4]);
    gpio_irq1_clear_pin(gid,val1,val2);
  }
  else if (strncmp(name, "gpio_irq1_clear_all",20) == 0) {
    if (nargs != 4) {
      nargs_error(name,4);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    gpio_irq1_clear_all(gid,val1);
  }
  else if (strncmp(name, "gpio_irq0_enable",17) == 0) {
    if (nargs != 6) {
      nargs_error(name,6);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    uint32 val2 = parse_num(args[4]);
    uint32 val3 = parse_num(args[5]);
    gpio_irq0_enable(gid,val1,val2,val3);
  }
  else if (strncmp(name, "gpio_irq0_enable_pin",21) == 0) {
    if (nargs != 5) {
      nargs_error(name,5);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    uint32 val2 = parse_num(args[4]);
    gpio_irq0_enable_pin(gid,val1,val2);
  }
  else if (strncmp(name, "gpio_irq0_enable_all",21) == 0) {
    if (nargs != 4) {
      nargs_error(name,4);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    gpio_irq0_enable_all(gid,val1);
  }
  else if (strncmp(name, "gpio_irq1_enable",17) == 0) {
    if (nargs != 6) {
      nargs_error(name,6);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    uint32 val2 = parse_num(args[4]);
    uint32 val3 = parse_num(args[5]);
    gpio_irq1_enable(gid,val1,val2,val3);
  }
  else if (strncmp(name, "gpio_irq1_enable_pin",21) == 0) {
    if (nargs != 5) {
      nargs_error(name,5);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    uint32 val2 = parse_num(args[4]);
    gpio_irq1_enable_pin(gid,val1,val2);
  }
  else if (strncmp(name, "gpio_irq1_enable_all",21) == 0) {
    if (nargs != 4) {
      nargs_error(name,4);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    gpio_irq1_enable_all(gid,val1);
  }
  else if (strncmp(name, "gpio_irq0_disable",18) == 0) {
    if (nargs != 6) {
      nargs_error(name,6);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    uint32 val2 = parse_num(args[4]);
    uint32 val3 = parse_num(args[5]);
    gpio_irq0_disable(gid,val1,val2,val3);
  }
  else if (strncmp(name, "gpio_irq0_disable_pin",22) == 0) {
    if (nargs != 5) {
      nargs_error(name,5);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    uint32 val2 = parse_num(args[4]);
    gpio_irq0_disable_pin(gid,val1,val2);
  }
  else if (strncmp(name, "gpio_irq0_disable_all",22) == 0) {
    if (nargs != 4) {
      nargs_error(name,4);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    gpio_irq0_disable_all(gid,val1);
  }
  else if (strncmp(name, "gpio_irq1_disable",18) == 0) {
    if (nargs != 6) {
      nargs_error(name,6);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    uint32 val2 = parse_num(args[4]);
    uint32 val3 = parse_num(args[5]);
    gpio_irq1_disable(gid,val1,val2,val3);
  }
  else if (strncmp(name, "gpio_irq1_disable_pin",22) == 0) {
    if (nargs != 5) {
      nargs_error(name,5);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    uint32 val2 = parse_num(args[4]);
    gpio_irq1_disable_pin(gid,val1,val2);
  }
  else if (strncmp(name, "gpio_irq1_disable_all",22) == 0) {
    if (nargs != 4) {
      nargs_error(name,4);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    gpio_irq1_disable_all(gid,val1);
  }
  else if (strncmp(name, "gpio_resetdone",15) == 0) {
    if (nargs != 3) {
      nargs_error(name,3);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    print_res(gpio_resetdone(gid));
  }
  else if (strncmp(name, "gpio_module_enable",19) == 0) {
    if (nargs != 3) {
      nargs_error(name,3);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    gpio_module_enable(gid);
  }
  else if (strncmp(name, "gpio_module_disable",20) == 0) {
    if (nargs != 3) {
      nargs_error(name,3);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    gpio_module_disable(gid);
  }
  else if (strncmp(name, "gpio_module",12) == 0) {
    if (nargs != 3) {
      nargs_error(name,3);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    print_res(gpio_module(gid));
  }
  else if (strncmp(name, "gpio_gatingratio_write",23) == 0) {
    if (nargs != 4) {
      nargs_error(name,4);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    gpio_gatingratio_write(gid,val1);
  }
  else if (strncmp(name, "gpio_gatingratio",17) == 0) {
    if (nargs != 3) {
      nargs_error(name,3);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    print_res(gpio_gatingratio(gid));
  }
  else if (strncmp(name, "gpio_pin_output",16) == 0) {
    if (nargs != 5) {
      nargs_error(name,5);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    uint32 val2 = parse_num(args[4]);
    gpio_pin_output(gid,val1,val2);
  }
  else if (strncmp(name, "gpio_pin_output_pin",20) == 0) {
    if (nargs != 4) {
      nargs_error(name,4);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    gpio_pin_output_pin(gid,val1);
  }
  else if (strncmp(name, "gpio_pin_output_all",20) == 0) {
    if (nargs != 3) {
      nargs_error(name,3);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    gpio_pin_output_all(gid);
  }
  else if (strncmp(name, "gpio_pin_input",15) == 0) {
    if (nargs != 5) {
      nargs_error(name,5);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    uint32 val2 = parse_num(args[4]);
    gpio_pin_input(gid,val1,val2);
  }
  else if (strncmp(name, "gpio_pin_input_pin",19) == 0) {
    if (nargs != 4) {
      nargs_error(name,4);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    gpio_pin_input_pin(gid,val1);
  }
  else if (strncmp(name, "gpio_pin_input_all",19) == 0) {
    if (nargs != 3) {
      nargs_error(name,3);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    gpio_pin_input_all(gid);
  }
  else if (strncmp(name, "gpio_pin",9) == 0) {
    if (nargs != 5) {
      nargs_error(name,5);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    uint32 val2 = parse_num(args[4]);
    print_res(gpio_pin(gid,val1,val2));
  }
  else if (strncmp(name, "gpio_pin_pin",13) == 0) {
    if (nargs != 4) {
      nargs_error(name,4);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    print_res(gpio_pin_pin(gid,val1));
  }
  else if (strncmp(name, "gpio_pin_all",13) == 0) {
    if (nargs != 3) {
      nargs_error(name,3);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    print_res(gpio_pin_all(gid));
  }
  else if (strncmp(name, "gpio_read",10) == 0) {
    if (nargs != 5) {
      nargs_error(name,5);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    uint32 val2 = parse_num(args[4]);
    print_res(gpio_read(gid,val1,val2));
  }
  else if (strncmp(name, "gpio_read_pin",14) == 0) {
    if (nargs != 4) {
      nargs_error(name,4);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    print_res(gpio_read_pin(gid,val1));
  }
  else if (strncmp(name, "gpio_read_all",14) == 0) {
    if (nargs != 3) {
      nargs_error(name,3);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    print_res(gpio_read_all(gid));
  }
  else if (strncmp(name, "gpio_write",11) == 0) {
    if (nargs != 6) {
      nargs_error(name,6);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    uint32 val2 = parse_num(args[4]);
    uint32 val3 = parse_num(args[5]);
    gpio_write(gid,val1,val2,val3);
  }
  else if (strncmp(name, "gpio_write_pin",15) == 0) {
    if (nargs != 5) {
      nargs_error(name,5);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    uint32 val2 = parse_num(args[4]);
    gpio_write_pin(gid,val1,val2);
  }
  else if (strncmp(name, "gpio_write_all",15) == 0) {
    if (nargs != 4) {
      nargs_error(name,4);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    gpio_write_all(gid,val1);
  }
  else if (strncmp(name, "gpio_irq_lowlevel_enable",25) == 0) {
    if (nargs != 5) {
      nargs_error(name,5);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    uint32 val2 = parse_num(args[4]);
    gpio_irq_lowlevel_enable(gid,val1,val2);
  }
  else if (strncmp(name, "gpio_irq_lowlevel_enable_pin",29) == 0) {
    if (nargs != 4) {
      nargs_error(name,4);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    gpio_irq_lowlevel_enable_pin(gid,val1);
  }
  else if (strncmp(name, "gpio_irq_lowlevel_enable_all",29) == 0) {
    if (nargs != 3) {
      nargs_error(name,3);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    gpio_irq_lowlevel_enable_all(gid);
  }
  else if (strncmp(name, "gpio_irq_lowlevel_disable",26) == 0) {
    if (nargs != 5) {
      nargs_error(name,5);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    uint32 val2 = parse_num(args[4]);
    gpio_irq_lowlevel_disable(gid,val1,val2);
  }
  else if (strncmp(name, "gpio_irq_lowlevel_disable_pin",30) == 0) {
    if (nargs != 4) {
      nargs_error(name,4);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    gpio_irq_lowlevel_disable_pin(gid,val1);
  }
  else if (strncmp(name, "gpio_irq_lowlevel_disable_all",30) == 0) {
    if (nargs != 3) {
      nargs_error(name,3);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    gpio_irq_lowlevel_disable_all(gid);
  }
  else if (strncmp(name, "gpio_irq_lowlevel",18) == 0) {
    if (nargs != 5) {
      nargs_error(name,5);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    uint32 val2 = parse_num(args[4]);
    print_res(gpio_irq_lowlevel(gid,val1,val2));
  }
  else if (strncmp(name, "gpio_irq_lowlevel_pin",22) == 0) {
    if (nargs != 4) {
      nargs_error(name,4);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    print_res(gpio_irq_lowlevel_pin(gid,val1));
  }
  else if (strncmp(name, "gpio_irq_lowlevel_all",22) == 0) {
    if (nargs != 3) {
      nargs_error(name,3);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    print_res(gpio_irq_lowlevel_all(gid));
  }
  else if (strncmp(name, "gpio_irq_highlevel_enable",26) == 0) {
    if (nargs != 5) {
      nargs_error(name,5);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    uint32 val2 = parse_num(args[4]);
    gpio_irq_highlevel_enable(gid,val1,val2);
  }
  else if (strncmp(name, "gpio_irq_highlevel_enable_pin",30) == 0) {
    if (nargs != 4) {
      nargs_error(name,4);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    gpio_irq_highlevel_enable_pin(gid,val1);
  }
  else if (strncmp(name, "gpio_irq_highlevel_enable_all",30) == 0) {
    if (nargs != 3) {
      nargs_error(name,3);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    gpio_irq_highlevel_enable_all(gid);
  }
  else if (strncmp(name, "gpio_irq_highlevel_disable",27) == 0) {
    if (nargs != 5) {
      nargs_error(name,5);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    uint32 val2 = parse_num(args[4]);
    gpio_irq_highlevel_disable(gid,val1,val2);
  }
  else if (strncmp(name, "gpio_irq_highlevel_disable_pin",31) == 0) {
    if (nargs != 4) {
      nargs_error(name,4);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    gpio_irq_highlevel_disable_pin(gid,val1);
  }
  else if (strncmp(name, "gpio_irq_highlevel_disable_all",31) == 0) {
    if (nargs != 3) {
      nargs_error(name,3);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    gpio_irq_highlevel_disable_all(gid);
  }
  else if (strncmp(name, "gpio_irq_highlevel",19) == 0) {
    if (nargs != 5) {
      nargs_error(name,5);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    uint32 val2 = parse_num(args[4]);
    print_res(gpio_irq_highlevel(gid,val1,val2));
  }
  else if (strncmp(name, "gpio_irq_highlevel_pin",23) == 0) {
    if (nargs != 4) {
      nargs_error(name,4);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    print_res(gpio_irq_highlevel_pin(gid,val1));
  }
  else if (strncmp(name, "gpio_irq_highlevel_all",23) == 0) {
    if (nargs != 3) {
      nargs_error(name,3);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    print_res(gpio_irq_highlevel_all(gid));
  }
  else if (strncmp(name, "gpio_irq_rising_enable",23) == 0) {
    if (nargs != 5) {
      nargs_error(name,5);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    uint32 val2 = parse_num(args[4]);
    gpio_irq_rising_enable(gid,val1,val2);
  }
  else if (strncmp(name, "gpio_irq_rising_enable_pin",27) == 0) {
    if (nargs != 4) {
      nargs_error(name,4);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    gpio_irq_rising_enable_pin(gid,val1);
  }
  else if (strncmp(name, "gpio_irq_rising_enable_all",27) == 0) {
    if (nargs != 3) {
      nargs_error(name,3);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    gpio_irq_rising_enable_all(gid);
  }
  else if (strncmp(name, "gpio_irq_rising_disable",24) == 0) {
    if (nargs != 5) {
      nargs_error(name,5);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    uint32 val2 = parse_num(args[4]);
    gpio_irq_rising_disable(gid,val1,val2);
  }
  else if (strncmp(name, "gpio_irq_rising_disable_pin",28) == 0) {
    if (nargs != 4) {
      nargs_error(name,4);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    gpio_irq_rising_disable_pin(gid,val1);
  }
  else if (strncmp(name, "gpio_irq_rising_disable_all",28) == 0) {
    if (nargs != 3) {
      nargs_error(name,3);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    gpio_irq_rising_disable_all(gid);
  }
  else if (strncmp(name, "gpio_irq_rising",16) == 0) {
    if (nargs != 5) {
      nargs_error(name,5);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    uint32 val2 = parse_num(args[4]);
    print_res(gpio_irq_rising(gid,val1,val2));
  }
  else if (strncmp(name, "gpio_irq_rising_pin",20) == 0) {
    if (nargs != 4) {
      nargs_error(name,4);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    print_res(gpio_irq_rising_pin(gid,val1));
  }
  else if (strncmp(name, "gpio_irq_rising_all",20) == 0) {
    if (nargs != 3) {
      nargs_error(name,3);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    print_res(gpio_irq_rising_all(gid));
  }
  else if (strncmp(name, "gpio_irq_falling_enable",24) == 0) {
    if (nargs != 5) {
      nargs_error(name,5);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    uint32 val2 = parse_num(args[4]);
    gpio_irq_falling_enable(gid,val1,val2);
  }
  else if (strncmp(name, "gpio_irq_falling_enable_pin",28) == 0) {
    if (nargs != 4) {
      nargs_error(name,4);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    gpio_irq_falling_enable_pin(gid,val1);
  }
  else if (strncmp(name, "gpio_irq_falling_enable_all",28) == 0) {
    if (nargs != 3) {
      nargs_error(name,3);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    gpio_irq_falling_enable_all(gid);
  }
  else if (strncmp(name, "gpio_irq_falling_disable",25) == 0) {
    if (nargs != 5) {
      nargs_error(name,5);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    uint32 val2 = parse_num(args[4]);
    gpio_irq_falling_disable(gid,val1,val2);
  }
  else if (strncmp(name, "gpio_irq_falling_disable_pin",29) == 0) {
    if (nargs != 4) {
      nargs_error(name,4);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    gpio_irq_falling_disable_pin(gid,val1);
  }
  else if (strncmp(name, "gpio_irq_falling_disable_all",29) == 0) {
    if (nargs != 3) {
      nargs_error(name,3);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    gpio_irq_falling_disable_all(gid);
  }
  else if (strncmp(name, "gpio_irq_falling",17) == 0) {
    if (nargs != 5) {
      nargs_error(name,5);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    uint32 val2 = parse_num(args[4]);
    print_res(gpio_irq_falling(gid,val1,val2));
  }
  else if (strncmp(name, "gpio_irq_falling_pin",21) == 0) {
    if (nargs != 4) {
      nargs_error(name,4);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    uint32 val1 = parse_num(args[3]);
    print_res(gpio_irq_falling_pin(gid,val1));
  }
  else if (strncmp(name, "gpio_irq_falling_all",21) == 0) {
    if (nargs != 3) {
      nargs_error(name,3);
      return 1;
    }
    gpioid8 gid = parse_num(args[2]);
    if (gid < 0 || gid > 3) {
      gid_error(gid);
    }
    print_res(gpio_irq_falling_all(gid));
  } else {
    fprintf(stderr, "Requested function call does not exist: %s\n",
        name);
    return 1;
  }
  return 0;
}

static void nargs_error(char* name, int expected) {
  fprintf(stderr, "Incorrect number of arguments for function call\n");
  fprintf(stderr, "\t%s needs %d arguments.\n", name, expected-2);
}

static void gid_error(gpioid8 gid) {
  fprintf(stderr, "Incorrect GPIO ID: %d\n");
  fprintf(stderr, "\tValid GPIO IDs: 0, 1, 2, 3\n");
}

static void print_res(uint32 res) {
  printf("Hex: %x\nDec: %d\n\n", res, res);
}

/*------------------------------------------------------------------------
 * parse - parse an argument that is either a decimal or hex value
 *------------------------------------------------------------------------
 */
static	uint32	parse_num(
	  char	*string			/* argument string to parse	*/
	)
{
	uint32	value;			/* value to return		*/
	char	ch;			/* next character		*/
	

	value = 0;

	/* argument string must consists of decimal digits or	*/
	/*	0x followed by hex digits			*/

	ch = *string++;
	if (ch == '0') {		/* hexadecimal */
		if (*string++ != 'x') {
			return 0;
		}
		for (ch = *string++; ch != NULLCH; ch = *string++) {
			if ((ch >= '0') && (ch <= '9') ) {
				value = 16*value + (ch - '0');
			} else if ((ch >= 'a') && (ch <= 'f') ) {
				value = 16*value + 10 + (ch - 'a');
			} else if ((ch >= 'A') && (ch <= 'F') ) {
				value = 16*value + 10 + (ch - 'A');
			} else {
				return 0;
			}
		}
	} else {			/* decimal */
		while (ch != NULLCH) {
			if ( (ch < '0') || (ch > '9') ) {
				return 0;
			}
			value = 10*value + (ch - '0');
			ch = *string++;
		}
	}
	return value;
}
