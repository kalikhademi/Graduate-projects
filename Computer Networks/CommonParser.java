import java.util.Scanner;
import java.io.File;
public class CommonParser {

    public int NumberOfPreferredNeighbors;
    public int UnchokingInterval;
    public int OptimisticUnchokingInterval;
    public String DataFileName;
    public int FileSize;
    public int PieceSize;

    public boolean Parse(String fileName){
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
                else
                    return false;
            }
            return true;
        }
        catch(Exception e){
            return false;
        }
    }

}

