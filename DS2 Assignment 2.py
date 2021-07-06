class Node:

	def __init__(self, item):
		
		self.item = item
		self.color = 1	# Black=0, Red=1
		self.parent = None
		self.leftChild = None
		self.rightChild = None

class RBT:

	def __init__(self):
		
		self.TNULL = Node(0)
		self.TNULL.color = 0
		self.TNULL.leftChild = None
		self.TNULL.rightChild = None
		self.root = self.TNULL
		self.treeSize = 0; # Initialize Tree Size

	def getHeight(self, node):
		
		if not(node.leftChild is None or node.rightChild is None):

			leftChildSize = self.getHeight(node.leftChild)
			rightChildSize = self.getHeight(node.rightChild)
			if leftChildSize > rightChildSize:
				x = leftChildSize + 1
				return x
			else:
				x = rightChildSize + 1
				return x

		else:

			return 0		# Height of Tree = Zero

	def getSize(self):
		
		return self.treeSize

	def search(self, node, key):
		
		if node == self.TNULL or key == node.item:
			return node

		if key < node.item:
			return self.search(node.leftChild, key)
		return self.search(node.rightChild, key)

	def rotateLeft(self, x):
		
		y = x.rightChild
		x.rightChild = y.leftChild
		if y.leftChild != self.TNULL:
			y.leftChild.parent = x

		y.parent = x.parent
		if x.parent == None:
			self.root = y
		elif x == x.parent.leftChild:
			x.parent.leftChild = y
		else:
			x.parent.rightChild = y
		y.leftChild = x
		x.parent = y

	def rotateRight(self, x):
		
		y = x.leftChild
		x.leftChild = y.rightChild
		if y.rightChild != self.TNULL:
			y.rightChild.parent = x

		y.parent = x.parent
		if x.parent == None:
			self.root = y
		elif x == x.parent.rightChild:
			x.parent.rightChild = y
		else:
			x.parent.leftChild = y
		y.rightChild = x
		x.parent = y

	def insertFix(self, k):

		while k.parent.color == 1:

			if k.parent == k.parent.parent.rightChild:

				u = k.parent.parent.leftChild
				if u.color == 1:
					u.color = 0
					k.parent.color = 0
					k.parent.parent.color = 1
					k = k.parent.parent
				else:
					if k == k.parent.leftChild:
						k = k.parent
						self.rotateRight(k)
					k.parent.color = 0
					k.parent.parent.color = 1
					self.rotateLeft(k.parent.parent)

			else:
				u = k.parent.parent.rightChild

				if u.color == 1:
					u.color = 0
					k.parent.color = 0
					k.parent.parent.color = 1
					k = k.parent.parent
				else:
					if k == k.parent.rightChild:
						k = k.parent
						self.rotateLeft(k)
					k.parent.color = 0
					k.parent.parent.color = 1
					self.rotateRight(k.parent.parent)

			if k == self.root:
				break

		self.root.color = 0

	def insert(self, key):

		self.treeSize += 1

		node = Node(key)
		node.parent = None
		node.item = key
		node.leftChild = self.TNULL
		node.rightChild = self.TNULL
		node.color = 1

		y = None
		x = self.root

		while x != self.TNULL:
			y = x
			if node.item < x.item:
				x = x.leftChild
			else:
				x = x.rightChild

		node.parent = y
		if y == None:
			self.root = node
		elif node.item < y.item:
			y.leftChild = node
		else:
			y.rightChild = node

		if node.parent == None:
			node.color = 0
			return

		if node.parent.parent == None:
			return

		self.insertFix(node)

	def deleteFix(self, x):
		
		while x != self.root and x.color == 0:
			if x == x.parent.leftChild:
				s = x.parent.rightChild
				if s.color == 1:
					s.color = 0
					x.parent.color = 1
					self.rotateLeft(x.parent)
					s = x.parent.rightChild

				if s.leftChild.color == 0 and s.rightChild.color == 0:
					s.color = 1
					x = x.parent
				else:
					if s.rightChild.color == 0:
						s.leftChild.color = 0
						s.color = 1
						self.rotateRight(s)
						s = x.parent.rightChild

					s.color = x.parent.color
					x.parent.color = 0
					s.rightChild.color = 0
					self.rotateLeft(x.parent)
					x = self.root
			else:
				s = x.parent.leftChild
				if s.color == 1:
					s.color = 0
					x.parent.color = 1
					self.rotateRight(x.parent)
					s = x.parent.leftChild

				if s.rightChild.color == 0 and s.rightChild.color == 0:
					s.color = 1
					x = x.parent
				else:
					if s.leftChild.color == 0:
						s.rightChild.color = 0
						s.color = 1
						self.rotateLeft(s)
						s = x.parent.leftChild

					s.color = x.parent.color
					x.parent.color = 0
					s.leftChild.color = 0
					self.rotateRight(x.parent)
					x = self.root
		x.color = 0

	def rbTransplant(self, u, v):

		if u.parent == None:
			self.root = v
		elif u == u.parent.leftChild:
			u.parent.leftChild = v
		else:
			u.parent.rightChild = v
		v.parent = u.parent

	def minimum(self, node):

		while node.leftChild != self.TNULL:
			node = node.leftChild
		return node

	def delete(self, node, key):

		z = self.TNULL
		while node != self.TNULL:
			if node.item == key:
				z = node

			if node.item <= key:
				node = node.rightChild
			else:
				node = node.leftChild

		if z == self.TNULL:
			print("\nERROR: Word Not in Dictionary!")	# Display a Message if Word to Delete isn't in Tree
			return

		self.treeSize -= 1
		print("\nWord Deleted!")						# Display a Message

		y = z
		y_original_color = y.color
		if z.leftChild == self.TNULL:
			x = z.rightChild
			self.rbTransplant(z, z.rightChild)
		elif (z.rightChild == self.TNULL):
			x = z.leftChild
			self.rbTransplant(z, z.leftChild)
		else:
			y = self.minimum(z.rightChild)
			y_original_color = y.color
			x = y.rightChild
			if y.parent == z:
				x.parent = y
			else:
				self.rbTransplant(y, y.rightChild)
				y.rightChild = z.rightChild
				y.rightChild.parent = y

			self.rbTransplant(z, y)
			y.leftChild = z.leftChild
			y.leftChild.parent = y
			y.color = z.color

		if y_original_color == 0:
			self.deleteFix(x)

if __name__ == "__main__":

	rbTree = RBT() 																# Initialize Tree

	while (True):

		ans = input("\nChoose an Option:\n-----------------\n[1] Load Dictionary('Dictionary.txt')\n[2] Search a Word\n[3] Insert New Word\n[4] Delete a Word\n[5] Show Dictionary Size and Height\n[6] Exit\n\nans = ")
		
		if ans == '1':

			words = open('Dictionary.txt').read().splitlines()					# Load File

			for i in words:														
				if ( rbTree.search(rbTree.root, i) == rbTree.TNULL ):			# Check if Word Already Exists in Tree
					rbTree.insert(i)											# Insert Each Word into The Tree
				else:
					print("\nERROR: '" + i + "' Already in Dictionary!")		# Display a Message


			print("\nDictionary Loaded!")										# Display a Message
			print( "\nTree Size: " + str(rbTree.getSize()) )					# Print Number of Elements in Tree
			
			treeHeight = rbTree.getHeight(rbTree.root)							# Get Tree Height
			if treeHeight == 0:
				print("Tree Height: 0")
			else:
				print("Tree Height: " + str(treeHeight-1))						# Print Tree Height

		elif ans == '2':

			key = input("\nWord to search: ")									# Take Word To Search For From User
			
			if ( rbTree.search(rbTree.root, key) == rbTree.TNULL ):				# Check if User's Word Exists in Tree
				print("\nNO")													# Display a Message
			else:
				print("\nYES")													# Display a Message

		elif ans == '3':

			key = input("\nWord to Insert: ")									# Take Word To Insert From User
			
			if ( rbTree.search(rbTree.root, key) == rbTree.TNULL ):				# Check if User's Word Already Exists in Tree
				
				rbTree.insert(key)												# Insert User's Word if it Doesn't Already Exist
				print("\nWord Inserted!")										# Display a Message
				print( "\nTree Size: " + str(rbTree.getSize()) )				# Print Number of Elements in Tree
				
				treeHeight = rbTree.getHeight(rbTree.root)						# Get Tree Height
				if treeHeight == 0:
					print("Tree Height: 0")
				else:
					print("Tree Height: " + str(treeHeight-1))					# Print Tree Height
			
			else:
				
				print("\nERROR: Word Already in Dictionary!")					# Display a Message
				print( "\nTree Size: " + str(rbTree.getSize()) )				# Print Number of Elements in Tree
				
				treeHeight = rbTree.getHeight(rbTree.root)						# Get Tree Height
				if treeHeight == 0:
					print("Tree Height: 0")
				else:
					print("Tree Height: " + str(treeHeight-1))					# Print Tree Height

		elif ans == '4':

			if rbTree.treeSize == 0:											# Check if Tree is Empty
				
				print("\nERROR: Tree is Empty")									# Display a Message
			
			else:
				
				key = input("\nWord to Delete: ")								# Take Word to Delete From User
				rbTree.delete(rbTree.root, key)									# Delete Word From Dictionary
				print( "\nTree Size: " + str(rbTree.getSize()) )				# Print Number of Elements in Tree
				
				treeHeight = rbTree.getHeight(rbTree.root)						# Get Tree Height
				if treeHeight == 0:
					print("Tree Height: 0")
				else:
					print("Tree Height: " + str(treeHeight-1))					# Print Tree Height

		elif ans == '5':

			print( "\nTree Size: " + str(rbTree.getSize()) )					# Print Number of Elements in Tree
			
			treeHeight = rbTree.getHeight(rbTree.root)							# Get Tree Height
			if treeHeight == 0:
				print("Tree Height: 0")
			else:
				print("Tree Height: " + str(treeHeight-1))						# Print Tree Height

		elif ans == '6':

			break																# Exit Program

		else:

			print('\nInvalid Option\n')											# Display a Message if Outside Range