
Members of group: Kiana Alikkhademi, Isabel Laurenceau, Mahya Aghaee

# To run this code:
1. Go to folder directory in terminal
2. Run "make clean" 
3. Run "make" to compile all the necessary java classes
3. Run "java peerProcess [peerID]" i.e "java peerProcess 1001"


# Architecture 
The main architecture of this project consists of the following main parts:

The top level is the peerProcess. There is only one thread of peerProcess running per client. PeerProcess extracts all necessary information from Common.cfg and PeerInfo.cfg using helper functions PeerParser and CommonParser. 
	*PeerParser: Parse the information of each paper by reading the peerInfo.cfg file
	*CommonParser: Same thing happens here. CommonParser read the info from common.cfg and save it into proper variables. 
	
Next we have Client. There is only one instance and thread of client as well. Client is made of multiple uploader and connection threads. Within the Client class, all the unchoking/choking timers are set. 
	*Uploader: Uploader listens on the TCP connection and passes the connection through the whole network. It's listener calls a new socket and starts a new thread for each connection. 
	*Connection: We need to track all the predefined connections to send the correct information toward the correct peer. All the different messages including piece, request, have, handshake, bitfield, interested and not interested have been implemented. 
	*DataFile: First, the original file splits into chunks of byte arrays. When the peers are done with downloading all the pieces of data, the data chunks will be merged into a file and stored in the proper directory. 

