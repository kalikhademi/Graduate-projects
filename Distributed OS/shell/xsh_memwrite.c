#include <xinu.h>
#include <string.h>
#include <stdio.h>

static uint32 parseval(char *);

shellcmd xsh_memwrite(int nargs, char *args[])
{
  if (nargs != 3) {
    fprintf(stderr, "%s addr value\n", args[0]);
    return 1;
  }

  uint32 *addr, val;
  addr = (uint32*)parseval(args[1]);
  val = parseval(args[2]);

  printf("Writing %x to %x\n", val, addr);

  *addr = val;
  return 0;
}

/*------------------------------------------------------------------------
 * parse - parse an argument that is either a decimal or hex value
 *------------------------------------------------------------------------
 */
static	uint32	parseval(
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
