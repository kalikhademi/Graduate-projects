import java.net.*;
import java.io.*;
import java.nio.*;
import java.nio.channels.*;
import java.util.*;
import java.util.logging.*;


public class peerProcess{
	public static int fileSize;
	public static int pieceSize;
    public static int numInPeerInfo;
    public static int portNum;
    public static boolean hasFile;
    public static int unchokingInterval;
    public static int optimisticUnchokingInterval;
    public static String fileName;
    public static ArrayList<byte[]> DataChunks;
    public static int numOfPreferredNeighbors; 


	public static void main(String args[] ){
        //Setting up logger.
        Logger rootLogger = Logger.getLogger("");
        for(Handler h : rootLogger.getHandlers()){
            rootLogger.removeHandler(h);
        }
        try {
            FileHandler hndlr = new FileHandler("log_peer_" + args[0] + ".txt");
            hndlr.setFormatter(new SimpleFormatter());
            rootLogger.addHandler(hndlr);
        }
        catch (IOException e){
            System.out.println(e.getMessage());
        }
        catch (ArrayIndexOutOfBoundsException e){
            System.out.println("Peer Process: first argument to peerProcess must be peerID.");
            System.exit(-1); //exit with error code -1 to indicate missing peerID.
        }
        rootLogger.info("Logger Setup.");
        String peerIDString = "";

		System.out.println("Peer Process: Starting Peer Process");

		// check for peerID 
        if (args.length > 0) { 
            for (String val:args) {
                System.out.println("Peer Process: PeerID " + val);
                peerIDString = val; 
            }
        } 
        else
            System.out.println("Peer Process: No peerID provided"); 
            boolean readFile = false;
            //read in files
            CommonParser CP = new CommonParser();
        if(CP.Parse("Common.cfg")){
            System.out.println("Peer Process: numOfPreferredNeighbors "+ CP.NumberOfPreferredNeighbors);
            numOfPreferredNeighbors = CP.NumberOfPreferredNeighbors;
            System.out.println("Peer Process: unchokingInterval "+CP.UnchokingInterval);
            unchokingInterval = CP.UnchokingInterval;
            System.out.println("Peer Process:  optimisticUnchokingInterval"+CP.OptimisticUnchokingInterval);
            optimisticUnchokingInterval = CP.OptimisticUnchokingInterval;
            System.out.println("Peer Process: fileName "+CP.DataFileName);
            fileName = CP.DataFileName;
            System.out.println("Peer Process: fileSize "+CP.FileSize);
            fileSize = CP.FileSize;
            System.out.println("Peer Process: pieceSize "+CP.PieceSize);
            pieceSize = CP.PieceSize;
        }
        else
        {
            System.out.println("Peer Process: Could not read Common.cfg file!");
        }


        
        // separate file into chunks
        // FileManager fileManager = new FileManager();
        // fileManager.fileSize = fileSize;
        // fileManager.pieceSize = pieceSize; 
        // fileManager.fileName = fileName;
        // fileManager.determineSizes();
        // try{
        // 	fileManager.splitFile();
        // }catch(IOException ioe){
        // 	System.out.print(" Could not split file from peer process: " + ioe);
        // }
        

        //read tracker 
        
        PeerParser PP = new PeerParser();
        numInPeerInfo = 0;
        int i = 0; 
        if(PP.Parse("PeerInfo.cfg")){
            for(PeerParser.PeerInfo PI : PP.PeerInfos){
                System.out.print("Peer Process: " + PI.PeerID + " ");
                System.out.print(PI.HostName + " ");
                System.out.print(PI.Port + " ");
                System.out.println(PI.HasFile);
                
                if (PI.PeerID == Integer.parseInt(args[0])) {
                    readFile = PI.HasFile;
                    numInPeerInfo = i; 
                    portNum = PI.Port;
                    hasFile = PI.HasFile;
                }
                i++;
            }
        }
        else{
            System.out.println("Peer Process: Could not read PeerInfo.cfg!");
        }
        DataFile DF = new DataFile(CP.PieceSize, CP.FileSize);
        //make directories
        
        DF.makeDir(peerIDString);

        
        if(readFile){
            if(DF.ReadFileIntoChunks(CP.DataFileName)){
                DataChunks = DF.DataInChunks;
                System.out.println("Peer Process 1: the data chunks size is: "+DF.DataInChunks.size());
                // System.out.println(DF.DataInChunks.get(DF.DataInChunks.size() - 1).length);
            }
            else{
                System.out.println("Peer Process: Failed to load the data file!");
            }
        }

        int peerID = Integer.parseInt(peerIDString);
        int numOfPieces = (int) Math.ceil((double)fileSize/pieceSize);
        Client client = new Client();
        client.peerID = peerID;
        client.numInPeerInfo = numInPeerInfo; 
        client.port = portNum;
        client.fileSize = fileSize;
        client.pieceSize = pieceSize;
        client.hasFile = hasFile;
        client.fileName = fileName;
        client.unchokingInterval = unchokingInterval;
        client.numOfPreferredNeighbors = numOfPreferredNeighbors;
        client.optimisticUnchokingInterval = optimisticUnchokingInterval;

        if(DataChunks!= null){
            // System.out.println("the data chunks is :"+DataChunks);
            client.DataChunks = DataChunks; 
            for(int j=0; j < numOfPieces; j++){
                // System.out.println("the data chunks are:"+DataChunks.get(j));
            }
        }else{
            // DataFile df = new DataFile(pieceSize,fileSize);
            DF.makeEmpty();
            client.DataChunks = DF.DataInChunks;
            System.out.println("Peer Process 2: the data chunks size is: "+ client.DataChunks.size());
        }
        client.dataFile = DF;
        Thread object = new Thread(client);
        object.start();

        
    }
}