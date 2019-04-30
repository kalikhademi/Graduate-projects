// Node class
class AVLnode {
	// Variables
	AVLnode leftChild;
	AVLnode rightChild;
	AVLnode parent;
	
	int ID;
	int count;
	int height;
	
	// Constructors
	// Default
	AVLnode() {
		leftChild = null;
		rightChild = null;
		parent = null;
		ID = -1;
		count = -1;
		height = 0;
	}
	
	// Only constructor for ID, count
	AVLnode(int ID, int count) {
		leftChild = null;
		rightChild = null;
		parent = null;
		this.ID = ID;
		this.count = count;
		height = 0;
	}
	
	// Methods
	protected void updateAll() {
		updateChildParent();
		updateHeight();
	}
	
	protected void updateHeight() {
		this.height = 0;
		if (leftChild != null) {
			this.height = leftChild.height + 1;
		}
		if (rightChild != null) {
			this.height = Math.max(rightChild.height + 1, this.height);
		}
	}
	
	protected int getHeightDifference() {
		int leftHeight = -1;
		int rightHeight = -1;
		if (leftChild != null) leftHeight = leftChild.height;
		if (rightChild != null) rightHeight = rightChild.height;
		return leftHeight - rightHeight;
	}
	
	protected void updateChildParent() {
		if (leftChild != null)
			leftChild.parent = this;
		if (rightChild != null)
			rightChild.parent = this;
	}
	
}

// AVL tree handler
public class AVL {
	// Variables
	AVLnode root;
	boolean doRotate = true;
	
	// Constructors
	AVL() {
		root = null;
	}
	
	AVL(int[] IDs, int[] counts) {
		// Make a balanced BST from a sorted list
		// Get middle of array as root, recursively do the same for left/right children
		root = internalInitialize(IDs, counts, 0, IDs.length - 1);
	}
	
	// Recursive method for O(n) initialize
	private AVLnode internalInitialize(int[] IDs, int[] counts,
			int startIndex, int endIndex) {
		
		// Default/ran out of room case
		if (startIndex > endIndex) {
			return null;
		}
		
		// Find midpoint, make new node for it
		int midpoint = (startIndex + endIndex) / 2;
		AVLnode newNode = new AVLnode(IDs[midpoint], counts[midpoint]);
		
		// Recursive left and right children
		newNode.leftChild = internalInitialize(IDs, counts, startIndex, midpoint - 1);
		newNode.rightChild = internalInitialize(IDs, counts, midpoint + 1, endIndex);

		// Update height and children's parent pointers
		newNode.updateAll();
		
		// Return for recursion
		return newNode;
	}
	
	// Methods
	
	// Insert and increase use same methodology
	public void insert(int ID, int count) {	
		internalInsert(ID, count);
	}
	public void increase(int ID, int m) {	
		// Insert's duplicate ID case handles increasing.
		internalInsert(ID, m);
	}
	
	// Internal insert/increase method, not recursive
	private void internalInsert(int ID, int count) {
		// Variables
		AVLnode currentNode = root;
		AVLnode previousNode = null;
		boolean wentLeft = false;
		boolean stop = false;
		int heightDiff;
		
		// Walk through tree until we can insert/increase
		while (currentNode != null && currentNode.ID != ID) {
			// Update previous node
			previousNode = currentNode;
			
			// Go left or right
			if (currentNode.ID > ID) {
				currentNode = currentNode.leftChild;
				wentLeft = true;
				
			} else {
				currentNode = currentNode.rightChild;
				wentLeft = false;
				
			}
		}
		
		// Where did we stop?
		if (currentNode != null) {
			// Node already exists, update value
			currentNode.count += count;
			
		} else {
			// Must create new node
			currentNode = new AVLnode(ID, count);
			
			if (previousNode == null) {
				// New root node
				root = currentNode;
				
			} else {
				if (wentLeft) {
					// New left child
					previousNode.leftChild = currentNode;
					
				} else {
					// New right child
					previousNode.rightChild = currentNode;
					
				}
				
				// Update height and children's parent pointers
				previousNode.updateAll();
			}
		}
		
		// Print results
		System.out.println(currentNode.count);
		
		// Walk backwards and adjust heights
		currentNode = previousNode;
		while(!stop && currentNode != null) {			
			// Update node's height
			currentNode.updateHeight();
			heightDiff = currentNode.getHeightDifference();
			
			// If we are rotating and the height difference is too much
			if (doRotate && Math.abs(heightDiff) == 2) {
				// After rotating we can stop
				stop = true;
				
				// Rotate as necessary
				// LL
				if (currentNode.ID > ID && currentNode.leftChild != null && currentNode.leftChild.ID >= ID) {
					currentNode = rotateClockwise(currentNode);				
					
				// RR
				} else if (currentNode.ID < ID && currentNode.rightChild != null && currentNode.rightChild.ID <= ID) {
					currentNode = rotateCounterClockwise(currentNode);
					
				// LR
				} else if (currentNode.ID > ID && currentNode.leftChild != null && currentNode.leftChild.ID <= ID) {
					currentNode.leftChild = rotateCounterClockwise(currentNode.leftChild);
					currentNode = rotateClockwise(currentNode);

				// RL
				} else { //if (currentNode.ID < ID && currentNode.rightChild != null && currentNode.rightChild.ID >= ID) {
					currentNode.rightChild = rotateClockwise(currentNode.rightChild);
					currentNode = rotateCounterClockwise(currentNode);
				}
				
			} else if (heightDiff == 0) { 
				// Stop early
				stop = true;
			}
			
			if (currentNode.parent == null) {
				root = currentNode;
			}
			
			currentNode = currentNode.parent;
		}		
	}
	
	// Not recursive
	public void reduce(int ID, int m) {
		internalReduce(ID, m);
	}
	
	private void internalReduce(int ID, int count) {
		// Variables
		AVLnode currentNode = root;
		AVLnode previousNode = null;
		boolean wentLeft = false;
		boolean stop = false;
		int heightDiff;
		
		// Walk through tree until we can reduce/remove
		while (currentNode != null && currentNode.ID != ID) {
			// Update previous node
			previousNode = currentNode;
			
			// Go left or right
			if (currentNode.ID > ID) {
				currentNode = currentNode.leftChild;
				wentLeft = true;
				
			} else {
				currentNode = currentNode.rightChild;
				wentLeft = false;
				
			}
		}
		
		// Where did we stop?
		if (currentNode != null) {
			// Node exists, update value
			currentNode.count -= count;
			
			if (currentNode.count > 0) {
				System.out.println(currentNode.count);
				
			} else { // count <= 0
				System.out.println("0");
				
				// Remove node
				// Case two children
				if (currentNode.leftChild != null && currentNode.rightChild != null) {
					// Find next smallest.
					AVLnode replacement = currentNode.leftChild;
					wentLeft = true;
					while (replacement.rightChild != null) {
						replacement = replacement.rightChild;
						wentLeft = false;
					}
					
					// swap values with the replacement
					currentNode.ID = replacement.ID;
					currentNode.count = replacement.count;
					
					// Now remove replacement node
					currentNode = replacement;
					previousNode = replacement.parent;
					
				} 
				
				// Case one child, if and not else-if to allow for replaced two child case
				if (currentNode.leftChild != null) {
					currentNode = currentNode.leftChild;
					
				// Case one child or leaf node.
				} else {
					currentNode = currentNode.rightChild;					
				
				}
								
				// Update previous node to point to replacement
				if (previousNode == null) {
					root = currentNode;
					
				} else {
					if (wentLeft) {
						previousNode.leftChild = currentNode;
						
					} else {
						previousNode.rightChild = currentNode;
						
					}
					
					// Update height/children's parent pointers
					previousNode.updateAll();
				}
				
				// Walk back up and rotate as necessary
				currentNode = previousNode;
				while (!stop && currentNode != null) {
					currentNode.updateHeight();
					heightDiff = currentNode.getHeightDifference();
					
					// If we are rotating and the height difference is too much
					if (doRotate && Math.abs(heightDiff) == 2) {
						// L-based
						if (currentNode.ID > ID) {
							heightDiff = currentNode.rightChild.getHeightDifference();
							// L0 
							if (heightDiff == 0) {
								currentNode = rotateCounterClockwise(currentNode);
								stop = true;
								
							// L1
							} else if (heightDiff == -1)	{
								currentNode = rotateCounterClockwise(currentNode);
							
							// L-1
							} else { // heightDiff == 1
								currentNode.rightChild = rotateClockwise(currentNode.rightChild);
								currentNode = rotateCounterClockwise(currentNode);
								
							}
						
						// R-based
						} else { //if (currentNode.ID < ID) {
							heightDiff = currentNode.leftChild.getHeightDifference();
							// R0 
							if (heightDiff == 0) {
								currentNode = rotateClockwise(currentNode);
								stop = true;
								
							// R1
							} else if (heightDiff == 1)	{
								currentNode = rotateClockwise(currentNode);
							
							// R-1
							} else { // heightDiff == -1
								currentNode.leftChild = rotateCounterClockwise(currentNode.leftChild);
								currentNode = rotateClockwise(currentNode);
								
							}
						}
						
						
					} else if (Math.abs(heightDiff) == 1) {
						// Stop early
						stop = true;
					}
					
					// Update height/children's parent pointers
					currentNode.updateAll();
					
					if (currentNode.parent == null) {
						root = currentNode;
					}
					
					currentNode = currentNode.parent;
				}
			}
		} else {
			// Node does not exist
			System.out.println("0");
		}
	}
	
	// Recursive method for count
	public void count(int ID) {
		System.out.println(internalCount(ID, root));
	}
	
	private int internalCount(int ID, AVLnode node) {
		if (node == null) {
			return 0;
		} else if (ID == node.ID) {
			return node.count;
		} else if (ID < node.ID) {
			return internalCount(ID, node.leftChild);
		} else { // ID > node.ID
			return internalCount(ID, node.rightChild);
		}
	}

	// Method for next, not recursive
	public void next(int ID) {
		internalNext(ID);
		
	}
	
	private AVLnode internalNext(int ID) {
		AVLnode current = root;
		boolean stop = false;
		boolean found = false;
		
		if (current != null) {
			// Run to where it would be in the tree
			while (!stop && current.ID != ID) {
				if (ID < current.ID) {
					if (current.leftChild != null)
						current = current.leftChild;
					else
						stop = true;
				} else {
					if (current.rightChild != null)
						current = current.rightChild;
					else
						stop = true;
				}
			}
			
			// Don't count if currentID is the ID
			// If currentID is less than ID, we've found it
			if (current.ID != ID) {
				if (current.ID > ID)
					found = true;
			}
			
			// Back up until we can go right, stop if we come from left once,
			//  don't go right if it's the direction we came from
			int previousID = ID;
			
			while (!found && 
				   (current.rightChild == null || 
					current.rightChild.ID == previousID) && 
					current.parent != null) {
				
				if (current.parent.leftChild != null && current.parent.leftChild.ID == current.ID)
					found = true;
				
				previousID = current.ID;
				current = current.parent;
			}
			
			// If we did not find it by backtracking left once and there is a right child
			//  and we did not come from that right child
			if (!found && current.rightChild != null && 
					current.rightChild.ID != previousID) {
				
				// go right once
				current = current.rightChild;
			
				// Go left until cannot go any more.
				while (current.leftChild != null)
					current = current.leftChild;
				
				found = true;
			}
		}
		
		if (found) {
			// Print current values
			System.out.println(current.ID + " " + current.count);
			
		} else {
			// Next does not exist
			System.out.println("0 0");
			current = null;
			
		}

		return current;
	}

	// Method for previous ID, not recursive
	public void previous(int ID) {
		internalPrevious(ID);
		
	}
	
	private AVLnode internalPrevious(int ID) {
		boolean stop = false;
		boolean found = false;
		AVLnode current = root;
		
		if (current != null) {
			// Run to where it would be in the tree
			while (!stop && current.ID != ID) {
				if (ID < current.ID) {
					if (current.leftChild != null)
						current = current.leftChild;
					else
						stop = true;
				} else {
					if (current.rightChild != null)
						current = current.rightChild;
					else
						stop = true;
				}
			}

			// Don't count if currentID is the ID
			// If currentID is greater than ID, we've found it
			if (current.ID != ID) {
				if (current.ID < ID)
					found = true;
			}
			
			// Back up until we can go left, stop if we come from right once,
			//  don't go left if it's the direction we came from
			int previousID = ID;
			
			while (!found && (current.leftChild == null || 
					current.leftChild.ID == previousID) && 
					current.parent != null) {
				if (current.parent.rightChild != null && current.parent.rightChild.ID == current.ID)
					found = true;
				
				previousID = current.ID;
				current = current.parent;
			}
			
			// If we did not find it by backtracking right once and there is a left child
			//  and we did not come from that left child
			if (!found && current.leftChild != null && 
					current.leftChild.ID != previousID) {
				
				// go left once
				current = current.leftChild;
			
				// Go right until cannot go any more.
				while (current.rightChild != null)
					current = current.rightChild;
				
				found = true;
			}
		}
		
		if (found) {
			// Print current values
			System.out.println(current.ID + " " + current.count);
			
		} else {
			// Next does not exist
			System.out.println("0 0");
			current = null;
			
		}
		
		return current;
		
	}

	// In range method, recursive
	public void inRange(int ID1, int ID2) {
		internalInRange(ID1, ID2, root);
		System.out.println();
	}
	
	private int internalInRange(int ID1, int ID2, AVLnode node) {
		// Base recursive case.
		if (node == null) {
			return 0;
		}
		int total = 0;
		
		// If node.ID > ID1, call left subtree
		if (node.ID > ID1) {
			total += internalInRange(ID1, ID2, node.leftChild);
		}
		
		// If node.ID in range, print node.ID
		if (node.ID >= ID1 && node.ID <= ID2) {
			total += node.count;
			System.out.print(node.count + " ");
		}
		
		// If node.ID < ID2, call right subtree
		if (node.ID < ID2) {
			total += internalInRange(ID1, ID2, node.rightChild);
		}
		
		return total;
		
	}
	

	// Rotations
	// Rotate once clockwise
	public AVLnode rotateClockwise(AVLnode node) {
		if (node == null) {
			return node;
		}
		AVLnode A = node;
		AVLnode B = node.leftChild;
		AVLnode grandParent = A.parent;
		AVLnode c = node.leftChild.rightChild;
		
		B.rightChild = A;
		A.leftChild = c;

		
		// update the height and parent pointers.
		B.parent = grandParent;
		if (grandParent != null) {
			if (grandParent.leftChild != null && grandParent.leftChild.ID == A.ID) {
				grandParent.leftChild = B;
			} else {
				grandParent.rightChild = B;
			}
		}
		A.updateAll();
		B.updateAll();
		
				
		return B;
	}
	
	// Rotate once counter-clockwise
	public AVLnode rotateCounterClockwise(AVLnode node) {
		if (node == null) {
			return node;
		}
		AVLnode A = node;
		AVLnode B = node.rightChild;
		AVLnode grandParent = A.parent;
		AVLnode c = node.rightChild.leftChild;
		
		B.leftChild = A;
		A.rightChild = c;
		
		// update the height and parent pointers.
		B.parent = grandParent;
		if (grandParent != null) {
			if (grandParent.leftChild != null && grandParent.leftChild.ID == A.ID) {
				grandParent.leftChild = B;
			} else {
				grandParent.rightChild = B;
			}
		}
		A.updateAll();
		B.updateAll();
				
		return B;
	}
	
	// For debugging purposes
	// Recursive method that walks the tree, in-order
	public void walk() {
		internalWalk(root);
	}
	
	private void internalWalk(AVLnode node) {
		if (node == null) return;
		else {
			internalWalk(node.leftChild);
			System.out.println("ID: " + node.ID);
			System.out.println("count: " + node.count);
			System.out.println("height: " + node.getHeightDifference());
			internalWalk(node.rightChild);
		}
	}
}