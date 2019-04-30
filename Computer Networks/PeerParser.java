import java.io.File;
import java.util.ArrayList;
import java.util.Scanner;

public class PeerParser {
    public class PeerInfo {
        public int PeerID;
        public String HostName;
        public int Port;
        public boolean HasFile;
        PeerInfo(int pid, String hname, int port, int hasfile){
            this.PeerID = pid;
            this.HostName = hname;
            this.Port = port;
            this.HasFile = hasfile  == 1 ;
        }
    }

    public ArrayList<PeerInfo> PeerInfos;

    boolean Parse(String fileName){
        try {
            File file = new File(fileName);
            Scanner sc = new Scanner(file);
            PeerInfos = new ArrayList<>();

            while(sc.hasNextLine()){
                PeerInfos.add(new PeerInfo(sc.nextInt(),sc.next(),sc.nextInt(),sc.nextInt()));
            }
            return true;
        }
        catch (Exception e){
            return false;
        }
    }

}
