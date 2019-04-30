import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class bbst {
	public static void main(String[] args) throws FileNotFoundException {
		// Variables
		File filePointer;
		File commandPointer;
		Scanner inputFile;
		Scanner input;		 
		int[] IDs;
		int[] counts;
		int n;
		int com1, com2;
		String command;
		AVL avlObj;
		
		// Check for args
		if (args.length >= 1) {
			filePointer = new File(args[0]);
			inputFile = new Scanner(filePointer);
			if (args.length == 2) {
				commandPointer = new File(args[1]);
				input = new Scanner(commandPointer);
				
			} else {
				input = new Scanner(System.in);
				
			}
		} else {
			System.out.println("file use: java bbst file-name");
			return;
		}
		
		// Open file, read IDs and counts
		n = inputFile.nextInt();
		IDs = new int[n];
		counts = new int[n];
		
		for (int i = 0; i < n; ++i) {
			IDs[i] = inputFile.nextInt();
			counts[i] = inputFile.nextInt();
		}
				
		// Efficient initialize of AVL
		avlObj = new AVL(IDs, counts);

		// Get user input
		do {
			command = input.next();
			
			// apply commands to AVL
			switch(command) {
			case "next":
				com1 = input.nextInt();
				System.out.println(command + " " + com1);
				avlObj.next(com1);
				break;
				
			case "count":
				com1 = input.nextInt();
				System.out.println(command + " " + com1);
				avlObj.count(com1);
				break;
				
			case "previous":
				com1 = input.nextInt();
				System.out.println(command + " " + com1);
				avlObj.previous(com1);
				break;
				
			case "increase" :
				com1 = input.nextInt();
				com2 = input.nextInt();
				System.out.println(command + " " + com1 + " " + com2);
				avlObj.increase(com1, com2);
				break;
				
			case "reduce" :
				com1 = input.nextInt();
				com2 = input.nextInt();
				System.out.println(command + " " + com1 + " " + com2);
				avlObj.reduce(com1, com2);
				break;
				
			case "inrange" :
				com1 = input.nextInt();
				com2 = input.nextInt();
				System.out.println(command + " " + com1 + " " + com2);
				avlObj.inRange(com1, com2);
				break;
			
			case "walk" :
				System.out.println(command);
				avlObj.walk();
				break;
				
			
			}
			
		} while (!command.equals("exit") && !command.equals("quit"));
		
		
		System.out.println(command);
		
		// Clean up
		input.close();
		inputFile.close();
		
	}
}
