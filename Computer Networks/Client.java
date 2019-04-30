import java.net.*;
import java.io.*;
import java.nio.*;
import java.nio.channels.*;
import java.util.*;
import java.util.logging.Logger;
import java.util.stream.IntStream;
import java.util.Arrays;
import java.net.InetAddress; //for hostname
import java.net.UnknownHostException; //for hostname
import java.util.LinkedList;
import java.util.Timer;
import java.util.TimerTask;
import java.util.Random;

//Client is yourself. You as a client have an uploader, file handler, peerLinkedList, and connectionLinkedList
public class Client implements Runnable{

	//My information
	public int peerID;
	public String hostName;
	public int port;
	public boolean hasFile;
	public LinkedList<Peer> peerLinkedList = new LinkedList<Peer>();
	public LinkedList<Connection> connectionLinkedList = new LinkedList<Connection>();
	public Socket connection;

	//from commmon.pg
	public int numInPeerInfo;
	public int fileSize;
  	public int pieceSize;
	public int unchokingInterval;
	public int optimisticUnchokingInterval;
	public static String fileName;
	
	public static int numOfPieces;
	public static byte myBitfield[];
	public DataFile dataFile ;
	public ArrayList<byte[]> DataChunks;

	public int numOfPreferredNeighbors;

 	Uploader up = new Uploader();
 	public boolean sentHandshake = false;
 	public boolean theBoolean = false;

 	public static boolean done;


 	private static Logger logger = Logger.getLogger("");

	//constructor
	public void Client(){}

	@Override
	public void run() {
		//start timers
		initalizeTimer();

		//set bitfield to correct size
		numOfPieces = (int) Math.ceil((double)fileSize/pieceSize);
		byte[] emptyArray = new byte[numOfPieces];
		
		myBitfield = emptyArray;

		System.out.println("Client: Run in client with peerID "+ this.peerID+ " with num in PeerInfo "+ numInPeerInfo);

		//tracker initalization
		addPeers();

		//start our listener/ uploader
		runUploader();
	}

	public void runUploader(){
		System.out.println("Client: Calling run uploader");
        if(hasFile == true){
			for(int j=0; j< myBitfield.length; j++){
				myBitfield[j] = 1;
			}
		}else{
			for(int j=0; j< myBitfield.length; j++){
				myBitfield[j] = 0;
			}
		}

		up.peerID = peerID;
		up.portNumber = port;
		up.hasFile = hasFile;
		up.myBitfield = myBitfield;
		up.fileSize = fileSize;
		up.pieceSize = pieceSize;
		up.fileName = fileName;
		up.unchokingInterval = unchokingInterval;
		up.optimisticUnchokingInterval = optimisticUnchokingInterval;
		up.numInPeerInfo = numInPeerInfo;
		up.peerLinkedList = peerLinkedList;
		up.connectionLinkedList = connectionLinkedList;
		up.numOfPieces = numOfPieces; 
		up.DataChunks = DataChunks;
		up.df = dataFile; 

		Thread object = new Thread(up);
		try{
			object.start();
		}catch(Exception e){
			System.err.println("Client: Exception: "+ e);
			done = true;
		}
	}

	public void addPeers(){
		System.out.println("Client: In addPeers()");

		//get info for peer and connection List
		PeerParser PP = new PeerParser();
        if(PP.Parse("PeerInfo.cfg")){
        	for(int i = 0; i < numInPeerInfo; i++){
            	PeerParser.PeerInfo PI = PP.PeerInfos.get(i);

            	//place all info in a peer object
            	Peer newPeer = new Peer();
                newPeer.peerID = PI.PeerID;
                newPeer.hostName = PI.HostName;
                newPeer.port = PI.Port;
                newPeer.hasFile =  PI.HasFile;
                newPeer.interested = false;
				newPeer.preferredNeighbor = false;
				newPeer.optimisticNeighbor = false;

				int numOfPieces = (int) Math.ceil((double)fileSize/pieceSize);
				byte[] emptyArray = new byte[numOfPieces];
				newPeer.bitfield = emptyArray;

				//add to Peer Linked List
				peerLinkedList.add(newPeer);


            	Connection newConnection = new Connection();
            	//their info
            	newConnection.peerID = PI.PeerID;
            	newConnection.hostname = PI.HostName;
            	newConnection.portNumber = PI.Port;
            	newConnection.hasFile = PI.HasFile;
            	newConnection.interested = false;
            	newConnection.preferredNeighbor = false;
            	newConnection.optimisticNeighbor = false;
				newConnection.peerBitfield = emptyArray;
				newConnection.fileName = fileName;

            	//my info
            	newConnection.sendersPeerID = peerID;
            	newConnection.sendersHostName = hostName;
            	newConnection.sendersPort = port; // this is currently listener will change
            	newConnection.sendersHasFile = hasFile;  // this is currently listener will change

            	newConnection.alone = false;
            	newConnection.sendHandshake = true;
            	newConnection.receivedHandshake = false;
		        newConnection.fileSize = fileSize;
		        newConnection.pieceSize = pieceSize;
		        newConnection.numOfPieces = numOfPieces;
		        newConnection.unchokingInterval = unchokingInterval;
		        newConnection.optimisticUnchokingInterval = optimisticUnchokingInterval;
		  
				newConnection.DataChunks = DataChunks;
				newConnection.dataFile = dataFile;  

		        newConnection.numInPeerInfo = numInPeerInfo;
		        
		        if(newConnection.sendersHasFile == true){
					for(int j=0; j< myBitfield.length; j++){
						myBitfield[j] = 1;
					}
				}else{
					for(int j=0; j< myBitfield.length; j++){
						myBitfield[j] = 0;
					}
				}
				newConnection.myBitfield = myBitfield;
				connectionLinkedList.add(newConnection);

				newConnection.peerLinkedList = peerLinkedList;
				newConnection.connectionLinkedList = connectionLinkedList;
            }
        }
        else{
            System.out.println("Could not read PeerInfo.cfg!");
        }
	}

	public void initalizeTimer(){
		//timer for choke and unchoke
		Timer unChokeTimer = new Timer();
		Timer optUnChokeTimer = new Timer();

		TimerTask unChoke = new TimerTask(){
			public void run(){
				unChoke(unchokingInterval);
			}
		};

		TimerTask optUnChoke = new TimerTask(){
			public void run(){
				optimisticUnchoke(optimisticUnchokingInterval);
			}
		};

		//timer is in miliseconds so we need to multiply by 1000
		long miliUnChoke = unchokingInterval *1000;
		long miliOptUnChoke = optimisticUnchokingInterval *1000;

		unChokeTimer.schedule(unChoke, miliUnChoke);
		optUnChokeTimer.schedule(optUnChoke,miliOptUnChoke);
	}

	//preferred neighbor choke timer
	public void updateChokeTimer(){
		Timer unChokeTimer = new Timer();
		try{
			checkIfDone();
		}catch(InterruptedException iE){
			System.err.println("Client: check if done error " + iE);
		}
		
		
		TimerTask unChoke = new TimerTask(){
			public void run(){
				unChoke(unchokingInterval);
			}
		};

		//timer is in miliseconds so we need to multiply by 1000
		long miliUnChoke = unchokingInterval *1000;
		unChokeTimer.schedule(unChoke, miliUnChoke);
	}

	public void unChoke(int unchokingInterval){
		// System.out.println(unchokingInterval + " seconds has passed normal unchoke/choke");
		try{
			updateChokeTimer();
			determinePreferredNeighbors();
		}catch(Exception e){
			System.err.print("Client: Unchoke Exception ");
			e.printStackTrace();
		}
	}

	public void determinePreferredNeighbors(){
		//update my peer Linked List
		peerLinkedList = up.peerLinkedList;
		connectionLinkedList = up.connectionLinkedList;

		System.out.println("Client: Determining Preferred Neighbors "+ peerLinkedList);

		//check to see if k is greater than size of connection list
		if(numOfPreferredNeighbors >= connectionLinkedList.size()){
			System.out.println("Client: k is greater than number of neighbors. Make all preferred");
			//make all neighbors in connection and peer list preffereed neighbors and unchoke
			for(int i = 0; i < peerLinkedList.size(); i++){
				peerLinkedList.get(i).preferredNeighbor = true;
			}
			for(int i = 0; i < connectionLinkedList.size(); i++){
				connectionLinkedList.get(i).preferredNeighbor = true;
				connectionLinkedList.get(i).sendUnchokeMessage();
			}
		//take the top k elements based on connectionLinkedList.get(i).connectionDownloadRate
		}else{
			//check if I have complete file if yes
			if(hasFile == true){
				//determines preferred neighbors randomly among those that are interested, not using download rates
				pickRandomNeighbors();
			}else{
				//take the top k elements based on connectionLinkedList.get(i).connectionDownloadRate
				pickKNeighbors();
			}
		}
	}

	public void pickKNeighbors() {
		System.out.println("Client: Picking new preferred neighbors");
		Connection[] tempConnectionArray = new Connection[connectionLinkedList.size()];
		tempConnectionArray = connectionLinkedList.toArray(tempConnectionArray);

		//select preferred neighbors --> sort tempConnectionLinkedList by connectionDownloadRate
		Arrays.sort(tempConnectionArray, new SortByRate());

		StringBuilder sb = new StringBuilder();
		for (int i = 0; i < numOfPreferredNeighbors; i++){
			if (i != 0)
				sb.append(',');
			sb.append(tempConnectionArray[i].peerID);
		}
		logger.info("Peer " + peerID + " has the preferred neighbors: " + sb.toString());



		int countOfK = 1;
		for(int i = 0; i < tempConnectionArray.length; i++){

			//preferred neighbors: check to see that peer is interested
			if(tempConnectionArray[i].interested == true && countOfK < numOfPreferredNeighbors){
				countOfK++;
				for(int j =0; j <connectionLinkedList.size(); j++){
					///TODO: if neighbor is not unchoked send unchoke message
					//need to get the correct connection to send from though
					if(connectionLinkedList.get(j).peerID == tempConnectionArray[j].peerID && connectionLinkedList.get(j).preferredNeighbor == false && connectionLinkedList.get(j).optimisticNeighbor == false){
						connectionLinkedList.get(j).sendUnchokeMessage();
					}
				}
			}

			//non preferred neighbors
			if(tempConnectionArray[i].interested == true && countOfK >= numOfPreferredNeighbors){
				//if neighbor was preferred but now is not send choke message // unless it is an optimistically unchoken neighbor
				if(connectionLinkedList.get(i).peerID == tempConnectionArray[i].peerID && connectionLinkedList.get(i).preferredNeighbor == true && connectionLinkedList.get(i).optimisticNeighbor == false){
						connectionLinkedList.get(i).sendChokeMessage();
				}
			}
		}
	}

	public void pickRandomNeighbors(){
		System.out.println("Client: I have the complete file. Picking Preferred Neighbors Randomly");

		try{
			//update my Linked Lists
			peerLinkedList = up.peerLinkedList;
			connectionLinkedList = up.connectionLinkedList;

			//actually make a random decision
			if(numOfPreferredNeighbors < peerLinkedList.size()){
				//make random assignment array
		        ArrayList<Integer> rand = new ArrayList<Integer>();
		        for(int i = 0; i < peerLinkedList.size(); i++){
		        	rand.add(i);
		        }
		        Collections.shuffle(rand);

		        ArrayList<Integer> oldPreferreds = new ArrayList<Integer>();
		        //make everyone not a preferred neighbor
		       	for(int i = 0; i < peerLinkedList.size(); i++){
		        	//check if preferred
		        	if(peerLinkedList.get(i).preferredNeighbor == true){
			        	peerLinkedList.get(i).preferredNeighbor = false;
			        	oldPreferreds.add(i);
			        }
		        }
		        //pick numOfPreferredNeighbors new preferred neighbors
		        for(int i = 0; i < numOfPreferredNeighbors; i++){
		        	//pick rand from range of peers use rand for that
		        	//check it's not an index you already picked
		        	int newPrefferedIndex = rand.get(i);
	        		//new preferred neighbor
	        		peerLinkedList.get(newPrefferedIndex).preferredNeighbor = true;
		        }
		        //send out choke message to people who are no longer preferred neighbors
		        for(int i = 0; i < connectionLinkedList.size(); i++ ){
		        	if(oldPreferreds.contains(i)==true){
		        		connectionLinkedList.get(i).sendChokeMessage();
		        	}
					if(peerLinkedList.get(i).preferredNeighbor == true && oldPreferreds.contains(i)==false){
	        			connectionLinkedList.get(i).sendUnchokeMessage();
		        	}
		        }
			}else{
				//make everyone a preferred neighbor
		       	for(int i = 0; i < numOfPreferredNeighbors; i++){
		        	//check if preferred.
		        	if(peerLinkedList.get(i).preferredNeighbor == false){
			        	peerLinkedList.get(i).preferredNeighbor = true;
			        	connectionLinkedList.get(i).sendUnchokeMessage();
			        }
				}
			}
		}catch(Exception e){
			System.out.print("pickRandomNeighbors Error: ");
			e.printStackTrace();
		}
	}

	//optimistically picked neighbor timer
	public void updateOptTimer(){
		Timer optUnChokeTimer = new Timer();
		
		try{
			checkIfDone();
		}catch(InterruptedException iE){
			System.err.println("Client: check if done error " + iE);
		}

		TimerTask optUnChoke = new TimerTask(){
			public void run(){
				optimisticUnchoke(optimisticUnchokingInterval);
			}
		};

		//timer is in miliseconds so we need to multiply by 1000
		long miliOptUnChoke = optimisticUnchokingInterval *1000;
		optUnChokeTimer.schedule(optUnChoke,miliOptUnChoke);

	}

	public void optimisticUnchoke(int optimisticUnchokingInterval){
		updateOptTimer();
		// System.out.println("Client: " + optimisticUnchokingInterval + " seconds has passed for optimistic Choke/Unchoke");
		try{
			//update my peer Linked List
			peerLinkedList = up.peerLinkedList;
			connectionLinkedList = up.connectionLinkedList;
			System.out.println("Client: Opt unchoking peer list "+ peerLinkedList);
			

			//if I am not alone
			if(connectionLinkedList.size() != 0){
				done = connectionLinkedList.get(0).done;
				//System.out.println("Client: Opt unchoking Done Value "+ done);
				if(done == false){
					//get current optimistic neighbor to change later
					int oldNeighbor = 0;
					for(int i = 0; i < connectionLinkedList.size(); i++){
						if(connectionLinkedList.get(i).preferredNeighbor == true || connectionLinkedList.get(i).optimisticNeighbor == true){
							oldNeighbor = i;
						}
					}

					if(peerLinkedList.size() == 1){
						//you only have one neighbor and should just keep as preferred unchoked neighbor
						//send choke message to old opt neighbor
						peerLinkedList.get(0).preferredNeighbor = true;

						//make optimistic neighbor false
						peerLinkedList.get(0).optimisticNeighbor = false;

						//send unchoke message using connection from connection list
						connectionLinkedList.get(0).sendUnchokeMessage();
					}else{
						//select my peer to unchoke --> must be currently choked and interested
						int optNeighborIndex =  pickRandomOptNeighbor();
						System.out.println("Client: Opt unchoking peer: "+ optNeighborIndex);
						System.out.println("Client: Opt choking connection: "+ oldNeighbor);

						logger.info("Peer " + peerID + " has optimistically unchoked peer " + connectionLinkedList.get(optNeighborIndex).peerID);
						//send unchoke message using connection from connection list
						connectionLinkedList.get(optNeighborIndex).sendUnchokeMessage();

						//send choke message to old opt neighbor
						connectionLinkedList.get(oldNeighbor).sendChokeMessage();

						//make old optimistic neighbor false
						peerLinkedList.get(oldNeighbor).optimisticNeighbor = false;
						connectionLinkedList.get(oldNeighbor).optimisticNeighbor = false;

						//propogate changes down stream too
						up.peerLinkedList = peerLinkedList;
						up.connectionLinkedList = connectionLinkedList;
					}
				}else{
					Thread.currentThread().interrupt();
					System.exit(1);
				}
			}
		}catch(Exception e){
			System.out.print("optimisticUnchoke: ");
			e.printStackTrace();
		}
	}

	public int pickRandomOptNeighbor(){
		//get number of peers
        int numOfPeers = connectionLinkedList.size();

        if(numOfPeers != 0 && numOfPeers!= 1){
	        //pick rand from range of peers use rand for that
	        int rand = new Random().nextInt(numOfPeers);
	        System.out.println("Client: Test random neighbor: " + rand);
	        //check that not already unchoked & that it is interested
	        System.out.println("Client: In Pick Opt Peer: " + connectionLinkedList.get(rand).peerID + " is interested: "+ connectionLinkedList.get(rand).interested + " is preferred " + connectionLinkedList.get(rand).preferredNeighbor+ " is optimistic " + connectionLinkedList.get(rand).optimisticNeighbor);

	        if(connectionLinkedList.get(rand).preferredNeighbor == false && connectionLinkedList.get(rand).optimisticNeighbor == false && connectionLinkedList.get(rand).interested == true){
	        	connectionLinkedList.get(rand).optimisticNeighbor = true;
	        	return rand;
	        }
	    }else if(numOfPeers == 1){
	        	if(connectionLinkedList.get(0).preferredNeighbor == false && connectionLinkedList.get(0).optimisticNeighbor == false && connectionLinkedList.get(0).interested == true){
	        	connectionLinkedList.get(0).optimisticNeighbor = true;
					return 0;
		    	}
		}else{
	    	//we have no peers	
		}
		return 0;
	}

	public void checkIfDone() throws InterruptedException {
		connectionLinkedList = up.connectionLinkedList;
		boolean allDone = true;
		if(connectionLinkedList.size() != 0){
			for(int i = 0; i < connectionLinkedList.size(); i++){
				if(connectionLinkedList.get(i).hasFile == false || connectionLinkedList.get(i).sendersHasFile == false ){
					allDone = false;
				}
				System.out.println("Client:Connection list member"+ connectionLinkedList.get(i).peerID == false + " peer has file "+ connectionLinkedList.get(i).hasFile + "I have the file "+ connectionLinkedList.get(i).sendersHasFile);
			}
			if(allDone == true){
				System.out.println("Client: All Done "+ connectionLinkedList.size());
				Thread.sleep(10000);
				System.exit(1);
			}
		}
		
	}
}