/*  main.c  - main */

#include <xinu.h>

int32	slot;			/* UDP slot to use		*/
uint32 remip = 3232235881;
uint32 remport = 9000;
uint32	localip;		/* local IP address to use	*/
uint32	remoteip;		/* remote IP address to use	*/
uint16	remoteport;		/* port number for UDP echo	*/
uint16	locport	= 52743;	/* local port to use		*/
sid32 rdata;

int int2str (int data, char *msg) {
	int msglen = 0;
	char revmsg[4] = {'0'};
	int i = 0;
	
	while (data != 0 && i < 4) {
		//printf("Data %d\n", data);
		revmsg[i] = (char)(data % 10 + '0');
		//printf("Get digit %c\n", revmsg[i]);
		data /= 10;
		i++;
		msglen++;

		//printf("Left data %d\n", data);
		//printf("Msg len %d\n", msglen);
	}

	int j = 0;
	while (i-- > 0) {
		msg[j] = revmsg[i];
		//printf("Get digit %c\n", msg[j]);
		j++;
	}
	return msglen;
}

void sendtmp(int data) {
	printf("Get temperature %d\n", data);
	int retries = 5;
	int retval;
	char msg[4] = {'0'};
	int msglen = int2str(data, msg);

	while (--retries > 0) {
		printf("send to ip %d port %d\n", remip, remoteport);
		retval = udp_sendto(slot, remip, remoteport, msg, msglen);
		if (retval == SYSERR) {
			kprintf("udp_sendto failed\n");
			continue;
		}
		kprintf("udp_sendto successful\n");
		break;
	}
}
void sendsound(int data) {
	printf("Get sound %d\n", data);
	int retries = 5;
	int retval;
	char msg[4] = {'0'};
	int msglen = int2str(data, msg);

	while (--retries > 0) {
		printf("send to ip %d port %d\n", remip, remoteport);
		retval = udp_sendto(slot, remip, remoteport, msg, msglen);
		if (retval == SYSERR) {
			kprintf("udp_sendto failed\n");
			continue;
		}
		printf("udp_sendto successful\n");
		break;
	}
}
void sendmag(int data) {
	printf("Get magnetic %d\n", data);
	int retries = 5;
	int retval;
	char msg[4] = {'0'};
	int msglen = int2str(data, msg);

	while (--retries > 0) {
		printf("send to ip %d port %d\n", remip, remoteport);
		retval = udp_sendto(slot, remip, remoteport, msg, msglen);
		if (retval == SYSERR) {
			printf("udp_sendto failed\n");
			continue;
		}
		printf("udp_sendto successful\n");
		break;
	}
}

process	main(void)
{
	recvclr();
	int retval;	/* return value	*/

	rdata = semcreate(1);
	

	localip = getlocalip();
	if (localip == SYSERR) {
		printf("could not obtain a local IP address\n");
		return SYSERR;
	}
	
	/* register local UDP port */
	slot = udp_register(0, 0, locport);
	if (slot == SYSERR) {
		printf("could not reserve UDP port %d\n", locport);
		return SYSERR;
	}
	printf("BBB listening on port %d\n", locport);

	/* Connect to the edge */
	while (1) {
		char msg[] = "192.168.1.101";
		retval = udp_sendto(slot, remip, remport, msg, 13);
		char	buff[1500];		/* buffer for incoming command	*/
		retval = udp_recvaddr(slot, &remoteip, &remoteport, buff, sizeof(buff), 3000);
		if (retval == TIMEOUT) {
			continue;
		} else if (retval == SYSERR) {
			continue;
		}
		break;
	}

	while (1) {
		char msg[] = "52743";
		retval = udp_sendto(slot, remip, remport, msg, 5);
		char	buff[1500];		/* buffer for incoming command	*/
		retval = udp_recvaddr(slot, &remoteip, &remoteport, buff, sizeof(buff), 3000);
		if (retval == TIMEOUT) {
			continue;
		} else if (retval == SYSERR) {
			continue;
		}
		break;
	}
		
	/* Do forever: read a command and send back data */	
	while (TRUE) {
		char	buff[1500];		/* buffer for incoming command	*/

		retval = udp_recvaddr(slot, &remoteip, &remoteport, buff, sizeof(buff), 600000);

		if (retval == TIMEOUT) {
			printf("timeout\n");
			continue;
		} else if (retval == SYSERR) {
			printf("error receiving UDP\n");
			continue;
		}
		if (buff[0] == 's') {
			printf("Start\n");
			if (buff[6] == 't') {
				printf("read tmp\n");
				wait(rdata);
				sendtmp(temperature_sensor_get_temprature_centigrade_blocking());
				signal(rdata);
			}
			if (buff[6] == 'm') {
				printf("read mag\n");
				wait(rdata);
				sendmag(magnetic_sensor_get());
				signal(rdata);
			}
			printf("End\n");
		} else if (buff[0] == 'L') {
			printf("Start\n");
			if (buff[5] == 'n') {
				printf("turn on LED\n");
				wait(rdata);
				uint8 actuator_set(1);
				printf("send to ip %d port %d\n", remip, remoteport);
				char msg[] = "on";
				retval = udp_sendto(slot, remip, remoteport, msg, 2);
				signal(rdata);
			}
			if (buff[5] == 'f') {
				printf("turn off LED\n");
				wait(rdata);
				uint8 actuator_set(0);
				printf("send to ip %d port %d\n", remip, remoteport);
				char msg[] = "off";
				retval = udp_sendto(slot, remip, remoteport, msg, 3);
				signal(rdata);
			}
			printf("End\n");
		} else if (buff[0] == 'e') {
			break;
		}
	}
	return OK;
}
