import java.net.*;
import java.io.*;
import java.nio.*;
import java.nio.channels.*;
import java.util.*;
import java.net.InetAddress; //for hostname
import java.net.UnknownHostException; //for hostname
import java.util.logging.Logger;

public class Connection extends Uploader implements Runnable{
	/**********************variables***********************/
	
	//If I am peer A this is peer B's info
	public  int peerID;
	public  String hostname;
	public  int portNumber;
	public  boolean hasFile;

	public boolean interested;
	public boolean preferredNeighbor;
	public boolean optimisticNeighbor;
	public byte[] peerBitfield; 

	//My Info 
	public static int sendersPeerID;
	public static String sendersHostName;
	public static int sendersPort;
	public static boolean sendersHasFile;
	public static byte[] myBitfield;

	public static boolean alone = true; 
	public static int fileSize;
    public static int pieceSize;
    public static int numOfPieces;
    public static String fileName; 
    public static int numInPeerInfo;
    public static int unchokingInterval;
    public static int optimisticUnchokingInterval;
    public static ArrayList<byte[]> DataChunks;
    public static DataFile dataFile;

	private byte[] message; 
	private byte[] bitfieldMessage; 
	private byte[] interestedMessage;
	private byte[] notInterestedMessage;
	private byte[] requestMessage;
	private byte[] haveMessage;    
	private byte[] chokeMessage;
	private byte[] unChokeMessage;
	private byte[] pieceMessage;
	private byte PieceIndex;
	private int chunksDownloaded = 0;
	public static  LinkedList<Connection> connectionLinkedList = new LinkedList<Connection>();
	public static  LinkedList<Peer> peerLinkedList = new LinkedList<Peer>();

    public Socket connection;
    private ObjectInputStream in;	//stream read from the socket
    private ObjectOutputStream out;    //stream write to the socket

    //for download rate
	private int chunksSinceUnchoked = 0; 
	public long connectionDownloadRate;
	private long startTimeSinceUnchoked;
	private long stopTimeSinceUnchoked;

	//handshake variables
	public static final int zerobits_size = 10;
	public static final int peerID_size = 4;
	public static final int header_size = 18;
	public static final int total_length = 32;
	public boolean sentHandshake = false;
	public boolean sendHandshake = false;
	public boolean receivedHandshake = false;

	private int lastRequestedIndex = 0; 

	public static boolean done = false;

	private static Logger logger = Logger.getLogger("");

	/********************** constructor ***********************/

	public void Connection (){}

	/********************** functions ***********************/
	
	//run establishes individual connection
	@Override
  	public void run() {
  		System.out.println("Connection: I am running");
  		initializeStreams();
  		
  		//either send out a handshake or check what message I got
		// if(sendHandshake == true){
		// 	System.out.println("Connection: I will send the handshake");
		// 	sendHandShake();
		// }

		try{	
			if (receivedHandshake == true){
	  			System.out.println("Connection: I am not alone");
	  			byte[] myObjects = (byte[])in.readObject();
  				getPeerID(myObjects);
  				addPeers();
  				sendBitfield();
	  		}

			while(true){
				//receive the message sent from the client
				byte[] myObjects = (byte[])in.readObject();
				checkMessage(myObjects);
			}
		}catch(ClassNotFoundException classnot){
			System.err.println("Connection: Data received in unknown format");
		}catch(IOException ioException){
			System.err.println("Connection: Disconnect with Client " + peerID);
			checkIfDone(fileName);
		}
	}

	public void initializeStreams(){
		System.out.println("Connection: I'm initializing streams");
		try{
			if (receivedHandshake == false && sendHandshake == true){ 
				connection = new Socket(hostname, portNumber);
				System.out.println("Connection: I'm setting up the connection");

				//logger.info("Conneting to peer " + peerID);
			}
			out = new ObjectOutputStream(connection.getOutputStream());
			out.flush(); //TODO ::: Do we need this?
			
			if (sendHandshake == true){
				sendHandShake();
			}
			in = new ObjectInputStream(connection.getInputStream());
		}catch (IllegalArgumentException exception) {
            System.err.println("Connection: Could not initalize streams 1: " + exception);
        }catch(IOException ioException){
			System.err.println("Connection: Could not initalize streams 2" + ioException);
		}
	}

	public void getPeerID(byte[] msg){
		//index of piece
		byte[] peerIDArray = new byte[4];
		System.arraycopy(msg, 28, peerIDArray, 0, 4);
		peerID = java.nio.ByteBuffer.wrap(peerIDArray).getInt();

		String msgString = new String(msg);
		System.out.println("Connection: msg: "+ msgString);
		System.out.println("Connection: PeerID: "+ peerID);	
	}

	//check message type
	public void checkMessage(byte[] msg){
		checkIfDone(fileName);
		byte messageValue = msg[4];
		
		System.out.println("Connection: message type: " + messageValue + " received from client: " + peerID);
		System.out.println("Connection: My bitfield ");
		for(int k = 0; k < myBitfield.length; k++){
			System.out.println(myBitfield[k]);
		}

		String message = new String (msg);
		
		while(true){
			switch (messageValue) {
		        case 0:
		        	System.out.println("Connection: received choke message received from client: " + peerID);
		            logger.info("Peer " + sendersPeerID + " received choke message from peer " + peerID);
		            stopTimeSinceUnchoked = System.currentTimeMillis();
		            break;
		        case 1:
		           	//received an unchoke message
		        	System.out.println("Connection: received unchoke message received from client: " + peerID);
		        	chunksSinceUnchoked = 0; 
		        	startTimeSinceUnchoked = System.currentTimeMillis();
		        	// create request
					logger.info("Peer " + sendersPeerID + " received unchoke message from peer " + peerID);
	        		sendRequest();
		            break;
		        case 2:
		        	System.out.println("Connection: received interested message from peer: "+ peerID);
					logger.info("Peer " + sendersPeerID + " received interested message from peer " + peerID);
		        	receivedInterseted();
		            break;
		        case 3:
		            System.out.println("Connection: received not interested message received from client: " + peerID);
					logger.info("Peer " + sendersPeerID + " received not interested message from peer " + peerID);
		            receivedNotInterseted();
		            break;
		        case 4:
		            System.out.println("Connection: received have message received from client: " + peerID);

					determineIfInterestedFromHave(msg);
		            break;
		        case 5:
		        	System.out.println("Connection: received bitfield message received from client: " + peerID);
		        		for(int k = 0; k < msg.length; k++){
							System.out.println(msg[k]);
						}
					logger.info("Peer " + sendersPeerID + " received bitfield message from peer " + peerID);
		            determineIfInterestedFromBitfield(msg);
		            break;
		        case 6:
		        	System.out.println("Connection: received request message received from client: " + peerID);
					logger.info("Peer " + sendersPeerID + " received request message from peer " + peerID);
		        	
		        	sendPiece(msg);
		            break;
		        case 7:
		        	System.out.println("Connection: received piece message received from client: " + peerID);
					logger.info("Peer " + sendersPeerID + " received piece message from peer " + peerID);
					 
		            receivedPiece(msg);

					stopTimeSinceUnchoked = System.currentTimeMillis();
		            break;
		       	case 73:
		           	System.out.println("Connection: received handshake message");
					logger.info("Peer " + sendersPeerID + " received handshake message from peer " + peerID);
		           	//getpeerID if needed. 
		           	//check if we sent our handshake? 
		           	boolean checkHandshake = CheckHandshake(msg); 
		           	if (sentHandshake == false && checkHandshake== true){
		           		receivedHandshake = true;
		           		getPeerID(msg);
		           		addPeers();
		           		sendHandShake();
		           	}
		           	
		            break;
		        default:
		            System.out.println("Connection: Not a valid type");
		            break;
		        }
				return;
		}
	}

	//send a message to the output stream
	public void sendMessage(byte[] msg){
 		if(done == false){
 			System.out.println("Connection: sending message: " + msg + " to Client " + peerID + " on port: "+ connection.getPort() + " at addres: "+ connection.getInetAddress().toString());
			try{				
				out.writeObject(msg);
				out.flush();
				System.out.println("Connection: message sent");
			}
			catch(IOException ioException){
				ioException.printStackTrace();
			}
		}
	}

	public boolean CheckHandshake(byte[] message){
		System.out.println("Connection: Check Handshake");
        byte[] msgHeader = new byte[header_size];
        byte[] msgID = new byte[peerID_size];
        byte[] msgZeroBits = new byte[zerobits_size];
        boolean flag = true;
        try{
            //store the different parts
            msgHeader = Arrays.copyOfRange(message, 0, header_size);
            msgZeroBits = Arrays.copyOfRange(message, header_size, header_size+zerobits_size);
            msgID = Arrays.copyOfRange(message, header_size +zerobits_size, total_length);
            int msgPeerID = java.nio.ByteBuffer.wrap(msgID).getInt();
            System.out.println("Connection: Check Handshake sent "+peerID+" and received "+ msgPeerID);

            if(msgPeerID != peerID){
            	System.out.println("Connection: The peerID from handshake is not correct");
                flag = false;
            }
        }catch(Exception e){
            e.printStackTrace();
        }
        return flag;
    }
    
	public void sendHandShake(){
		sentHandshake = true;	

		String handshake_zerobits = "0000000000";
		String handshake_header = "P2PFILESHARINGPROJ";
			
		sendersPort = connection.getLocalPort();
		sendersHostName = connection.getLocalAddress().toString();
		System.out.println("Connection: Sending Handshake from Connection to : " + hostname + " with port number "+ portNumber);
		System.out.println("Connection: My peerID is: " + sendersPeerID);
		System.out.println("Connection: My port number is: " + sendersPort);
		System.out.println("Connection: My hostname is: " + sendersHostName);
	
		//handshake
		message = new byte[32];
		
		System.arraycopy(handshake_header.getBytes(), 0, message,0, header_size);
		// System.out.println("handshake_header: "+ handshake_header);
		try {
	         String Str2 = new String(handshake_header.getBytes( "UTF-8" ));
	         // System.out.println("handshake_header Value: " + Str2 );
	         Str2 = new String (message);
	         // System.out.println("Message: " + Str2 );
	    } catch ( UnsupportedEncodingException e) {
	        System.err.println("Unsupported character set");
	    }

		
		System.arraycopy(handshake_zerobits.getBytes(), 0, message,header_size, zerobits_size);
		// System.out.println("handshake_zerobits: "+ handshake_zerobits);
		try {
	         String Str3 = new String(handshake_zerobits.getBytes( "UTF-8" ));
	         // System.out.println("handshake_zerobits Value: " + Str3 );
	         Str3 = new String (message);
	         // System.out.println("Message " + Str3 );
	    } catch ( UnsupportedEncodingException e) {
	         System.err.println("Unsupported character set");
	    }
		
		String peerIDString = Integer.toString(sendersPeerID); 

		byte[] peerIDByte = new byte[4];
		peerIDByte = ByteBuffer.allocate(4).putInt(sendersPeerID).array();

		System.arraycopy(peerIDByte, 0, message, header_size+zerobits_size, peerID_size);
		try {
	         String Str4 = new String(peerIDString.getBytes( "UTF-8" ));
	         // System.out.println("peerIDString Value: " + Str4 );
	         Str4 = new String (message);
	         // System.out.println("Message: " + Str4 );
	    } catch ( UnsupportedEncodingException e) {
	        System.err.println("Unsupported character set");
	    }

	    //send our messages
		sendMessage(message);

		//sendBitfield();

		if(done == false){
			System.out.println("Connection: Sending unchoke message from handshake");
			sendUnchokeMessage();
		}
	}

	public void addPeers(){
		//place all info in a peer object
    	Peer newPeer = new Peer();
        newPeer.peerID = peerID; 
        newPeer.hostName = hostname; 
        newPeer.port = portNumber;            
        newPeer.hasFile =  false; //assume false until proven wrong by receiving bitfield or have message 
        newPeer.interested = true; 
		newPeer.preferredNeighbor = true;
		newPeer.optimisticNeighbor = true;

		//assume empyty bitfield until proven wrong by receiving bitfield or have message 
		byte[] emptyArray = new byte[numOfPieces];
		newPeer.bitfield = emptyArray;
        
        peerLinkedList.add(newPeer);

     	System.out.println("Connection: Adding Peers Peers Linked List  " + peerLinkedList);
     	System.out.println("Connection: Adding Peers Connections Linked List " + connectionLinkedList);
	}

	public void sendBitfield(){
		//create payload
		//determine number of pieces from common.cfg
    	System.out.println("Connection: In sendBitfield with " + numOfPieces + " pieces to peer " + peerID);

		//determine what parts of the file I have 
		int length = 4 + 1 + numOfPieces; 
    	bitfieldMessage = new byte[length];
    	
		//create new bitfield message
		bitfieldMessage = ByteBuffer.allocate(length).putInt(length).array();
		bitfieldMessage[4] = 5;

		boolean sendBitBool = false;
    	if(sendersHasFile == true){
    		for (int i = 5; i< length; i++){
    			bitfieldMessage[i] =  1;
    			//send message to B
    		}
    	}

		for (int i = 0; i< numOfPieces; i++){
			if(myBitfield[i] == 1){
				sendBitBool = true;
			}
		}

		
		logger.info("Sending bitfield with " + numOfPieces + " pieces to peer " + peerID );
		if (sendBitBool){
			System.out.println("Connection: Sending Bitfield with " + numOfPieces + " pieces.");
			sendMessage(bitfieldMessage);
		}
	}

	public void receivedInterseted(){
		//update Peer to reflect that it is intersted in Peer List and Connection List

		//Peer List 
		for (int i = 0; i < peerLinkedList.size(); i++){
			if(peerID == peerLinkedList.get(i).peerID){
				peerLinkedList.get(i).interested = true;
			}
		}

		for (int i = 0; i < connectionLinkedList.size(); i++){
			if(peerID == connectionLinkedList.get(i).peerID){
				connectionLinkedList.get(i).interested = true; 
				System.out.println("Connection: Peer "+ peerID + " is interested: "+ connectionLinkedList.get(i).interested); 
			}
		}
	}

	public void receivedNotInterseted(){
		//update Peer to reflect that it is intersted in Peer List and Connection List
	
		//Peer List 
		for (int i = 0; i < peerLinkedList.size(); i++){
			if(peerID == peerLinkedList.get(i).peerID){
				peerLinkedList.get(i).interested = false;
			}
		}

		for (int i = 0; i < connectionLinkedList.size(); i++){
			if(peerID == connectionLinkedList.get(i).peerID){
				connectionLinkedList.get(i).interested = false; 
			}
		}
	}

	public void sendChokeMessage(){
		System.out.println("Connection: Sending Choke Message");

		//create new bitfield message
		int length = 5;
		chokeMessage = new byte[length];
	
	 	//initalize
		chokeMessage = ByteBuffer.allocate(length).putInt(length).array();
		chokeMessage[4] = 0;

		logger.info("Sending choke message to peer " + peerID);
		sendMessage(chokeMessage);
	}

	public void sendUnchokeMessage(){
		System.out.println("Connection: Sending UnChoke Message");

		//create new unchoke message
		int length = 5;
		unChokeMessage = new byte[length];
	
	 	//initalize
		unChokeMessage = ByteBuffer.allocate(length).putInt(length).array();
		unChokeMessage[4] = 1;
		logger.info("Sending Unchoke message to peer " + peerID);
		sendMessage(unChokeMessage);
	}

	public void determineIfInterestedFromHave(byte[] msg){
		System.out.println("Connection: Determining If Interested From Have");

		//index of piece
		byte[] indexByte = new byte[4];
		System.arraycopy(msg, 5, indexByte, 0, 4);
		int index = java.nio.ByteBuffer.wrap(indexByte).getInt();

		System.out.println("Connection: Peer " + sendersPeerID + " received have  message from peer " + peerID + " for piece " + index);
		logger.info("Peer " + sendersPeerID + " received have  message from peer " + peerID + " for piece " + index);

		peerBitfield[index] = 1; 
		boolean sendIntMes = false;
		
		//my bitfield 
		if(myBitfield[index] != 1){
			sendIntMes = true;  
		}
		if(sendIntMes == true){
			//if B has 1 where I have 0 sendInterestedMessage()
			sendInterestedMessage();
		}else{
			//else send sendNotInterestedMessage()
			sendNotInterestedMessage();
		}

		//check if peer's bitfield is complete
		boolean peerIsComplete = true;
		for(int i = 0; i < peerBitfield.length; i++){
			if(peerBitfield[i] == 0){
				peerIsComplete = false;
			}
		}
		//update hasFile if necessary
		if(peerIsComplete == true){
			hasFile = true;
		}
	}

	public void determineIfInterestedFromBitfield(byte[] msg){
		System.out.println("Connection: Determining If Interested From Bitfield");
	
		//determine if a neighbor has an interesting piece
		boolean sendIntMes = false;
		boolean peerIsComplete = true;
		System.out.println("peerBitfield");
		for (int i = 5; i< msg.length; i++){
			System.out.println(msg[i]);
			int bitIndex=i-5; 
			//update peer's bitfield
			peerBitfield[bitIndex] = msg[i];

			//compare our bitfields
			if(myBitfield[bitIndex] == 0 && msg[i] == 1){
				sendIntMes = true;  
			}
			if(msg[i] == 0){
				peerIsComplete = false;
			}
		}
		if(sendIntMes == true){
			//if B has 1 where I have 0 sendInterestedMessage()
			sendInterestedMessage();
		}else{
			//else send sendNotInterestedMessage()
			sendNotInterestedMessage();
		}
		//update hasFile if necessary
		if(peerIsComplete == true){
			hasFile = true;
		}
	}

	public void sendInterestedMessage(){
		System.out.println("Connection: Sending Interested Message");

		//create new bitfield message
		int length = 5;
		interestedMessage = new byte[length];
	
	 	//initalize
		interestedMessage = ByteBuffer.allocate(length).putInt(length).array();
		interestedMessage[4] = 2;
		logger.info("Sending interested to peer " + peerID);
		sendMessage(interestedMessage);
	}

	public void sendNotInterestedMessage(){
		System.out.println("Connection: Sending Interested Message");

		//create new bitfield message
		int length = 5;
		notInterestedMessage = new byte[length];
	
	 	//initalize
		notInterestedMessage = ByteBuffer.allocate(length).putInt(length).array();
		notInterestedMessage[4] = 3;

		sendMessage(notInterestedMessage);
	}

	public void sendRequest(){
		System.out.println("Connection: Sending Request Message");
		//if I do not have the file
		if(sendersHasFile == false){
			//create new request message
			int length = 9; //4 for length, 1 for type, 4 for payload
			requestMessage = new byte[length];
		
		 	//initalize
			requestMessage = ByteBuffer.allocate(length).putInt(length).array();
			requestMessage[4] = 6; //type six

			int rand = selectRandom(); 
			lastRequestedIndex = rand;
			System.out.println("Connection: Asking for piece: "+ rand);
			myBitfield[rand] = 2; 
			//requestMessage[5] = (byte) rand;

			byte[] indexByte = new byte[4];
			indexByte = ByteBuffer.allocate(4).putInt(rand).array();
			int index = java.nio.ByteBuffer.wrap(indexByte).getInt();

			System.arraycopy(indexByte, 0, requestMessage,5, 4);
			sendMessage(requestMessage);

			//start timer 
			startTimeSinceUnchoked = System.currentTimeMillis();
		}
	}

	public int selectRandom(){
		int r;
		do{
			r = new Random().nextInt(numOfPieces);
		}while(!((myBitfield[r] == 0 || myBitfield[r] == 2) && peerBitfield[r] == 1));

		return r;
	}

	public void sendPiece(byte[] msg){
		System.out.println("Connection: Sending Piece Message");		

		//index of piece
		byte[] indexByte = new byte[4];
		System.arraycopy(msg, 5, indexByte, 0, 4);
		int index = java.nio.ByteBuffer.wrap(indexByte).getInt();

		System.out.println("Connection: The index of piece to send is: "+ index);

		//create new piece message
		int length = 4 + 1 + 4+ pieceSize; //4 for length, 1 for type, 4 for index,  rest for piece content
		pieceMessage = new byte[length];
		byte[] data = new byte[pieceSize];

	 	//initalize
		pieceMessage = ByteBuffer.allocate(length).putInt(length).array();
		pieceMessage[4] = 7; //type seven

		if(myBitfield[index] == 1){
			data = DataChunks.get(index);
		}

		System.arraycopy(indexByte, 0, pieceMessage,5, indexByte.length);
		System.arraycopy(data, 0, pieceMessage,9, data.length);

		sendMessage(pieceMessage);
	}

	public void receivedPiece(byte[] msg){
		System.out.println("Connection: Received Piece Message");
		//update Peer to reflect that they get the piece 

		//get info from message		
		byte[] indexByte = new byte[4];
		System.arraycopy(msg, 5, indexByte, 0, 4);

		byte[] data = new byte[pieceSize];
		System.arraycopy(msg, 9, data,0, pieceSize);
		
		lastRequestedIndex = java.nio.ByteBuffer.wrap(indexByte).getInt();

		System.out.println("Connection: the msg is: "+ msg);
		System.out.println("Connection: the data is: "+ data);	
		System.out.println("Connection: The bitfield length is: " + myBitfield.length+ " and the index is: " + lastRequestedIndex);
		
		//check to make sure i don't already have it 
		if(myBitfield[lastRequestedIndex] == 0 || myBitfield[lastRequestedIndex] == 2){
			myBitfield[lastRequestedIndex] = 1;
		}
		
		DataChunks.set(lastRequestedIndex,data);
		logger.info("Peer " + sendersPeerID + " has downloaded the piece " + lastRequestedIndex + " from peer " + peerID);

		for(int i = 0; i < connectionLinkedList.size(); i++){
			connectionLinkedList.get(i).sendHave(lastRequestedIndex);
		}
		checkIfDone(fileName);
	}

	public void checkIfDone(String fName){
		//check if chunksDownloaded is the number of pieces we want
		// or if we started with the file and chunksDownloaded is zero check if hasFile is true		
		boolean bitFieldFull = true;
		for(int k = 0; k < myBitfield.length; k++){
			if(myBitfield[k] == 0 || myBitfield[k] == 2){
				bitFieldFull = false;
			}
		}

		if(bitFieldFull == true && done == false) {
			// DataFile df = new DataFile(pieceSize,fileSize);
			dataFile.WriteBytes(fName, sendersPeerID);
			System.out.println("Connection: File complete at time: " + System.currentTimeMillis());
			System.out.println("Connection: My bitfield ");
			for(int k = 0; k < myBitfield.length; k++){
				System.out.println(myBitfield[k]);
			}
		
			//check if all peers hasFile is true
			boolean allDone = true; 
			for(int i = 0; i < connectionLinkedList.size(); i++){
				System.out.println("Connection: Has peers "+ connectionLinkedList.get(i).peerID);
				if(connectionLinkedList.get(i).hasFile == false){
					allDone = false; 
					System.out.println("Connection: Peer "+ connectionLinkedList.get(i).peerID + " still has not finished.");
					System.out.println("Connection: Peer "+ connectionLinkedList.get(i).peerID + " bitfield: ");
					for(int k = 0; k < peerBitfield.length; k++){
						System.out.println(connectionLinkedList.get(i).peerBitfield[k]);
					}
				}
			}
			
			//stop program
			if(allDone == true && connectionLinkedList.size() != 0){
				done = true;
				System.out.println("Connection: Peer " + sendersPeerID + " has downloaded the complete file.");
				logger.info("Peer " + sendersPeerID + " has downloaded the complete file.");
				for(int k = 0; k < peerBitfield.length; k++){
						
					try{
						if(in != null){
							connectionLinkedList.get(k).in.close();
						}
						if(out != null){
							connectionLinkedList.get(k).out.close();
						}
						if (connection != null){
							connectionLinkedList.get(k).connection.close();
						}	
					 }catch(IOException ioException){
						System.err.println("Connection: Problem in check if done"+ ioException);
					}
				}
			}
		}
	}

	public void sendHave(int index){
		System.out.println("Connection: Sending Have Message");

		//create new bitfield message
		int length = 4 + 1+ 4;
		haveMessage = new byte[length];

	 	//initalize
		haveMessage = ByteBuffer.allocate(length).putInt(length).array();
		haveMessage[4] = 4;

		byte[] haveByte = new byte[4];
		haveByte = ByteBuffer.allocate(4).putInt(index).array();
		System.arraycopy(haveByte, 0, haveMessage,5, 4);

		System.out.println("Connection: I have the piece at index "+ index);

		sendMessage(haveMessage);
	}

	public long DetermineRate(){
		connectionDownloadRate =  chunksSinceUnchoked /(startTimeSinceUnchoked - stopTimeSinceUnchoked);
		return connectionDownloadRate;
	}

	public boolean getDone(){
		return done;
	}
}		