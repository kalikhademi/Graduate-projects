import java.net.*;
import java.io.*;
import java.nio.*;
import java.nio.channels.*;
import java.util.*;
import java.net.InetAddress; //for hostname
import java.net.UnknownHostException; //for hostname
import java.util.logging.Logger;

public class Uploader implements Runnable{
	
	public static int peerID;
	public static String hostname;
	public int portNumber;
	public static boolean hasFile;

	private static byte[] message;  //message send to the server
	private static byte interestedMessage[];
	private static byte notInterestedMessage[];
	private static byte[] requestMessage;         //message send to the server
	public static  LinkedList<Connection> connectionLinkedList = new LinkedList<Connection>();
	public static  LinkedList<Peer> peerLinkedList = new LinkedList<Peer>();

	public void Uploader (){}

	public static byte myBitfield[];

	public static boolean sentHandshake = false;
	public static int fileSize;
    public static int pieceSize;
    public static String fileName;
    public static int numOfPieces; 
    public static int numInPeerInfo;
    public static ArrayList<byte[]> DataChunks;
   	public static DataFile df; 

    public static int clientNum;
    public static int unchokingInterval;
    public static int optimisticUnchokingInterval;

    public Handler handler;

    public static boolean done;

    private static Logger logger = Logger.getLogger("");

	@Override
	public void run() {
		try{
			start();
		}catch(Exception e){
			System.out.println(e);
		}
	}
  	
  	public void start() throws Exception {
    	System.out.println("Uploader: I am starting on port: "+ portNumber);

        ServerSocket listener = new ServerSocket(portNumber);
		clientNum = 1;
		
		//check if you need to send a handshake and I have peers before me
		if(sentHandshake == false && numInPeerInfo != 0 ){
			for (int i = 0; i < peerLinkedList.size(); i++){
				System.out.println("Uploader: Trying to connect to peerID " + peerLinkedList.get(i).peerID+ " At port " + peerLinkedList.get(i).port+ " At host:  " + peerLinkedList.get(i).hostName);

				for (int j =0; j < connectionLinkedList.size(); j++){
					// if(connectionLinkedList.get(j).peerID == peerLinkedList.get(i).peerID){
						connectionLinkedList.get(j).sendHandshake = true;
						connectionLinkedList.get(j).receivedHandshake = false;
		      			Thread object = new Thread(connectionLinkedList.get(j));
		        		try{
							object.start();
						}catch(Exception e){
							System.err.println("Uploader: Exception: "+ e);
						}
					// }
				}
			}
			sentHandshake = true;
		}

    	try {
    		while(true) {
    			Socket peer = listener.accept();
				logger.info("Accepted connection from peer " + peerID);
    			handler = new Handler(peer,clientNum);
    			handler.start();
    			peerLinkedList = handler.newConnection.peerLinkedList;
    			connectionLinkedList = handler.newConnection.connectionLinkedList;
    			done = handler.newConnection.done;

    			System.out.println("Uploader: Client "  + clientNum + " is connected!");
    			System.out.println("Uploader: Accepted new connection from " + peer.getInetAddress() + " at port " + peer.getPort());
				
				clientNum++;
    		}
    	} finally {
        	// listener.close();
    	}
	}


	/**
 	* A handler thread class.  Handlers are spawned from the listening
 	* loop and are responsible for dealing with a single client's requests.
 	*/
	public static class Handler extends Thread {
		private Socket connection;
        private ObjectInputStream in;	//stream read from the socket
        private ObjectOutputStream out;    //stream write to the socket
		private int no;		//The index number of the client
		public Connection newConnection; 

		public Handler(Socket connection, int no) {
        	this.connection = connection;
    		this.no = no;
    	}

      	public void run() {
      		System.out.println("Uploader: In handler run");

      		//place all info in a peer object
        	Peer newPeer = new Peer();
            newPeer.peerID = 0; // 0 means unknown 
            newPeer.hostName = this.connection.getRemoteSocketAddress().toString();
            newPeer.port = this.connection.getPort();
            newPeer.hasFile =  false; //assume false until receive bitfield
            newPeer.interested = false;
			newPeer.preferredNeighbor = false;
			newPeer.optimisticNeighbor = false;

			int numOfPieces = (int) Math.ceil((double)fileSize/pieceSize);
			byte[] emptyArray = new byte[numOfPieces];
			newPeer.bitfield = emptyArray;

			//add to Peer Linked List
			peerLinkedList.add(newPeer);

      		//making this connection if I am first in tracker 
      		newConnection = new Connection();
      		newConnection.connection = this.connection;
      		
      		//their info 
      		newConnection.hostname = this.connection.getRemoteSocketAddress().toString();
      		newConnection.portNumber = this.connection.getPort();
      		newConnection.interested = false;
            newConnection.preferredNeighbor = false;
            newConnection.optimisticNeighbor = false;

			// byte[] emptyArray = new byte[numOfPieces];
			newConnection.peerBitfield = emptyArray;

      		//my info 
      		newConnection.sendersPeerID = peerID;
      		newConnection.sendersPort = connection.getLocalPort();
      		newConnection.sendersHostName = connection.getLocalAddress().toString();
      		newConnection.sendersHasFile = hasFile;
			newConnection.hasFile = false;
			newConnection.fileSize = fileSize;
			newConnection.pieceSize = pieceSize;
			newConnection.numOfPieces = numOfPieces; 
			newConnection.numInPeerInfo = numInPeerInfo;
			newConnection.unchokingInterval = unchokingInterval;
			newConnection.optimisticUnchokingInterval= optimisticUnchokingInterval;
			newConnection.peerLinkedList = peerLinkedList;
			newConnection.DataChunks = DataChunks;
			newConnection.dataFile = df; 
			connectionLinkedList.add(newConnection);
			newConnection.done = done;
			newConnection.connectionLinkedList = connectionLinkedList;
			newConnection.receivedHandshake = true;
			newConnection.sendHandshake = false;
			
			if(newConnection.sendersHasFile == true){
				for(int j=0; j< myBitfield.length; j++){
					myBitfield[j] = 1;
					// System.out.println("the bitfield from uploader is :"+ myBitfield[j]);
				}					
			}
			newConnection.myBitfield = myBitfield;

      		Thread object = new Thread(newConnection);
        	try{
				object.start();
			}catch(Exception e){
				System.out.println("Exception: "+ e);
				done = true;
				Thread.currentThread().interrupt();
			}
		}
	}		
}