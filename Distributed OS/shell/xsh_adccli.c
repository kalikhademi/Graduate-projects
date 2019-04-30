#include <xinu.h>
#include <string.h>
#include <stdio.h>

static uint32 parse_num(char* string);

void xsh_adccli_callback(uint32 pin, uint32 value) {
  printf("[CLBK] AIN%d: %d\n", pin, value);
}

shellcmd xsh_adccli(int nargs, char *args[])
{
  uint32 arg, pin;
  if (nargs == 2 && strncmp(args[1], "--help", 7) == 0) {
    printf("Use: %s pin_number\n\n", args[0]);
    printf("Description:\n");
    printf("\tPrints the value that was read from the given AIN pin.\n");
    return 0;
  }

  if (nargs == 2 && strncmp(args[1], "--init", 7) == 0) {
    adc_init();
    return 0;
  }

  if (nargs != 3) {
    fprintf(stderr, "%s: incorrect number of arguments\n", args[0]);
    fprintf(stderr, "Try '%s --help' for more information\n", args[0]);
    return 1;
  }

  arg = parse_num(args[2]);

  if (strncmp(args[1], "--callback", 11) == 0) {
    adc_invalidate_callback(arg,xsh_adccli_callback);
    return 0;
  }

  if (strncmp(args[1], "--block", 8) == 0) {
    adc_invalidate_blocking(arg);
    for (pin = 0; pin < 8; pin++) 
      printf("AIN%d: %d\n", pin, adc_value(pin));
  }

  return 0;
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
