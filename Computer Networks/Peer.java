import java.util.*;

public class Peer{
	//peer of current client 

	//peer info from tracker 
	public int peerID;
	public String hostName;
	public int port;
	public boolean hasFile;

	//peer info client wants to know
	public boolean interested;
	public boolean preferredNeighbor;
	public boolean optimisticNeighbor;
	public byte[] bitfield;
}