import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.io.File;
import java.io.BufferedReader;
import java.io.FileReader;
import static java.util.Arrays.copyOf;
import java.util.Properties;
import java.io.*;

public class DataFile {
    ArrayList<byte[]> DataInChunks = new ArrayList<>();
    ArrayList<File> FileList = new ArrayList<>();
    File file;

    int PieceSize;
    int FileSize;
    int numOfPieces = (int) Math.ceil((double)FileSize/PieceSize);
    DataFile(int pSize, int fSize){
        PieceSize = pSize;
        FileSize = fSize;
        numOfPieces = (int) Math.ceil((double)FileSize/PieceSize);
    }

    boolean ReadFileIntoChunks(String fileName){
        try {
            InputStream IS = new FileInputStream(fileName);
            int readBytes = 0;
            do{
                byte[] b = new byte[PieceSize];
                if( (readBytes = IS.read(b))  == PieceSize)
                    DataInChunks.add(b);
                else{
                    if(readBytes != -1)
                        DataInChunks.add(copyOf(b,readBytes));
                }
            } while(readBytes != -1);
            if(numOfPieces > DataInChunks.size()){
                for (int empties = DataInChunks.size(); empties < numOfPieces; empties++){
                    byte[] blanks = new byte[PieceSize];
                    DataInChunks.add(blanks);
                }
            }
            System.out.println("DataFile: The size of Data Array is: "+ DataInChunks.size());
            return true;
        }
        catch(Exception e)
        {
            return false;
        }
    }

    public void makeEmpty(){
        System.out.println("DataFile: numOfPieces = " + numOfPieces);
        for (int empties = 0; empties < numOfPieces; empties++){
            byte[] blanks = new byte[PieceSize];
            DataInChunks.add(blanks);
        }
        System.out.println("DataFile: The size of Data Array is: "+ DataInChunks.size());
    }

    public void makeDir(String peerID){
        String path = System.getProperty("user.dir");
        System.out.println("DataFile: Directory is "+ path);
        
        // boolean created = true; 
       
    
        String absolutePath = "";
        // String workingDirectory = System.getProperty("user.dir");
        
        //String peerIDString = Integer.toString(peerID);
        // System.out.println("the peerID is"+ peerIDString);
        absolutePath = path + File.separator + peerID;
        System.out.println("DataFile: Absolute directory is:"+ absolutePath);
        // System.out.println("the absolute path is : "+ absolutePath);
        try{
            Files.createDirectories(Paths.get(peerID));
        }catch(IOException ioE){
            System.err.println("DataFile: Could not make directory");
        }
       
    }

    public void WriteBytes(String fileName, int peerID){
        int i =0;
        try{
            String absolutePath = System.getProperty("user.dir") + File.separator + peerID;
            File file = new File(absolutePath, fileName);
            FileOutputStream output = new FileOutputStream(file);
            
            //write the bytes into the file
            System.out.println("the data chunks size is :"+ DataInChunks.size());
            for (int j = 0; j < DataInChunks.size();j++){
                output.write(DataInChunks.get(j));
                output.flush();
            }
            i++;
            BufferedReader br = new BufferedReader(new FileReader(absolutePath));     
            if (br.readLine() == null) {
                System.out.println("No errors, and file empty");
            }else{
                System.out.println("Not empty file");
            }
        }catch(Exception e){
             System.out.println("Exception: " + e); 
        }
    }
}
