import java.net.*;
import java.io.*;
import java.nio.*;
import java.nio.channels.*;
import java.util.*;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.Path;

public class FileManager{
	public static int fileSize;
	public static int pieceSize; 
	public static int maxPieceSize; 
	public static int windowSize; 
	public static String fileName;
	public static String workingDirectory;
	public static String absoluteFilePath;
	public static String dynamicName;
	public static HashMap<Integer, byte[]> bitfieldMap = new HashMap<Integer, byte[]>();

	public FileManager(){}

	public static void determineSizes(){
		//check to make sure pieceSize is not too large i.e. > 65536 bits in java because Babak told us. 
        maxPieceSize = 65536*8;
        if(pieceSize > maxPieceSize){
        	//make pieceSize equal to the max
        	pieceSize = maxPieceSize - 1; //minus one because we want a buffer space
        }

        windowSize = fileSize/10 ;
	}

	public static void splitFile() throws IOException{		 
		//get the file from the string
		Path currentRelativePath = Paths.get("");
		File file = new File(currentRelativePath.toAbsolutePath().toString()+"/"+fileName);

		//fileChunks are of size windowSize
		int num = fileSize; 
		int lastByteRead = 0;
		int start =0;
		int i= 0; //where we are in bitfield map
		byte[] fileChunkArray = new byte[windowSize];
		//read in the file
		try{
			FileInputStream fileInputStream = new FileInputStream(file);
			while(num > 0){
				if (num <= 5){
					windowSize = num;
				}
				// byte[] fileChunkArray = new byte[windowSize];
				
				lastByteRead = fileInputStream.read(fileChunkArray,0,windowSize);
				
				// start = start +windowSize;
				
				// String s1 = new String(fileChunkArray);
				System.out.print("the chunkarray length is :" + fileChunkArray.length);
				System.out.print("the lastbyte read is :"+ lastByteRead);
				// System.out.print("the fileChunk array is :"+ s1);
				bitfieldMap.put(lastByteRead,fileChunkArray);
				i++;
				dynamicName = fileName+ i;
				workingDirectory = System.getProperty("user.dir");
				absoluteFilePath = workingDirectory + File.separator + dynamicName;
				num = num - windowSize; 
				FileOutputStream newFile  = new FileOutputStream(absoluteFilePath);
				newFile.write(fileChunkArray);
				newFile.flush();
				newFile.close();

			}
			fileInputStream.close();	
		}catch(IOException ioe){
			System.out.println("Could not split file: " + ioe);
		}
	}
}