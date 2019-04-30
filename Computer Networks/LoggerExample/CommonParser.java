import java.util.Scanner;
import java.io.File;
import java.util.logging.Logger;
public class CommonParser {

    public int NumberOfPreferredNeighbors;
    public int UnchokingInterval;
    public int OptimisticUnchokingInterval;
    public String DataFileName;
    public int FileSize;
    public int PieceSize;

    public boolean Parse(String fileName){
        Logger logger = Logger.getLogger("");//since it is a single method class, we just defined it here.
        try {

            File file = new File(fileName);
            Scanner sc = new Scanner(file);

            while(sc.hasNext()){
                String temp = sc.next();
                if(temp.equals("NumberOfPreferredNeighbors")){
                    this.NumberOfPreferredNeighbors = sc.nextInt();
                }
                else if (temp.equals("UnchokingInterval")){
                    this.UnchokingInterval = sc.nextInt();
                }
                else if(temp.equals("OptimisticUnchokingInterval"))
                    this.OptimisticUnchokingInterval = sc.nextInt();
                else if(temp.equals("FileName"))
                    this.DataFileName = sc.next();
                else if(temp.equals("FileSize"))
                    this.FileSize = sc.nextInt();
                else if(temp.equals("PieceSize"))
                    this.PieceSize = sc.nextInt();
                else {
                    logger.severe("Cannot Parse Config File. Invalid Attribute Name in Config File.");
                    return false;
                }
            }

            logger.info("Parsed Config File Successfully.");
            return true;
        }
        catch(Exception e){
            logger.severe("Cannot Parse Config File. Invalid File (File not found probably).");
            return false;
        }
    }

}