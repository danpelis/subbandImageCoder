import PIL.Image
import numpy
from queue import PriorityQueue
import bitarray


image = PIL.Image.open('dennis.jpg')  
#image.show()
'''
Subband decomposition
'''
print("Separating Bands...")
rBand = list(image.getdata(0))
bBand = list(image.getdata(1))
gBand = list(image.getdata(2))
size = len(list(image.getdata()))
print(len(rBand))
print(len(bBand))
print(len(gBand))

'''
Scalar Quantization
'''
M = 256 # Num of image values
L = 18   # Quantization Levels 
t = []  # Transition Levels
r = []  # Reconstruction Levels

print("Calculating Transition Levels...")
for k in range (L + 1):
    t.append((M* ((2 * k) - 1))/(2 * L))
print(f"Steps: ${t}")

print("Calculating Reconstruction Levels...")
for k in range (L):
    r.append(int(((L - k) * M) / L))
r.reverse() 
print(f"Values: {r}")


def quantizeBand(band):
    newBand = []
    for pixel in band:
    if (pixel == t[0]):
        newBand.append(r[0])
    elif (pixel >= t[L]):
        newBand.append(r[L - 1])
    else:
        for k in range(L):
            if (t[k] < pixel <= t[k + 1]):
                newBand.append(r[k])
    return newBand

# newRBand = []
# for pixel in rBand:
#     if (pixel == t[0]):
#         newRBand.append(r[0])
#     elif (pixel >= t[L]):
#         newRBand.append(r[L - 1])
#     else:
#         for k in range(L):
#             if (t[k] < pixel <= t[k + 1]):
#                 newRBand.append(r[k])

# newBBand = []
# for pixel in bBand:
#     if (pixel == t[0]):
#         newBBand.append(r[0])
#     elif (pixel >= t[L]):
#         newBBand.append(r[L - 1])
#     else:
#         for k in range(L):
#             if (t[k] < pixel <= t[k + 1]):
#                 newBBand.append(r[k])

# newGBand = []
# for pixel in gBand:
#     if (pixel == t[0]):
#         newGBand.append(r[0])
#     elif (pixel >= t[L]):
#         newGBand.append(r[L - 1])
#     else:
#         for k in range(L):
#             if (t[k] < pixel <= t[k + 1]):
#                 newGBand.append(r[k])


# newImage = []
# for index, pixel in enumerate(rBand):
#     newImage.append((newRBand[index], newBBand[index], newGBand[index]))

# print("Creating Quantized Image")
# quantImage = PIL.Image.new(image.mode, image.size)
# quantImage.putdata(newImage)
# quantImage.show()



'''
Entropy Encoding
'''
print("Starting Entropy Encoding...")

def gatherSymbolProbs(band):
    symbolProbs = {}
    for val in band:
        if not val in symbolProbs:
            symbolProbs[val] = 1
        else:
            symbolProbs[val] += 1

    for key in symbolProbs:
        symbolProbs[key] = symbolProbs[key]/size

    return symbolProbs

class HuffTreeNode:
    def __init__(self, symbol, prob, left=None, right=None):
        self.symbol = symbol
        self.prob = prob
        self.left = None
        self.right = None
    def __repr__(self):
        return "HuffTreeNode(prob={})".format(self.prob)
    
    def __gt__(self, other):
        return self.prob > other.prob


def encode(root, symbol, huffmanCode):
  
    if (root == None):
        return
    # if(root.symbol == 85):
    #     # print(f"{root.prob}")
    #     # print(f"Left symbol: {root.right.symbol}")
    #     # print(f"Left prob: {root.left.prob}")
    #     # print(f"Right symbol: {root.right.symbol}")
    #     # print(f"Right prob: {root.right.prob}")
    if (root.left == None and root.right == None):
        huffmanCode[root.symbol] = symbol
    encode(root.left, f"{symbol}0", huffmanCode)
    encode(root.right, f"{symbol}1", huffmanCode)


def buildHuffmanTree(symbolProbs):
    # count frequency of appearance of each character
    # and store it in a map


    # Create a priority queue to store live nodes of Huffman tree
    # Notice that highest priority item has lowest frequency
    pq = PriorityQueue()

    print("Creating leaf nodes...")
    # Create a leaf node for each character and add it
    # to the priority queue.
    for symbol in symbolProbs:
        pq.put(HuffTreeNode(symbol, symbolProbs[symbol]))

    # do till there is more than one node in the queue
    print("Printing Huff Tree:")
    while (pq.qsize() > 1):
        # Remove the two nodes of highest priority
        # (lowest frequency) from the queue
        # print(pq.queue)
        left = pq.get()
        right = pq.get()
        # Create a new internal node with these two nodes as children 
        # and with frequency equal to the sum of the two nodes
        # frequencies. Add the new node to the priority queue.
        # print(f"left: {left}")
        # print(f"right: {right}")
        sum = left.prob + right.prob
        
        newNode = HuffTreeNode('\0', sum, left, right)
        newNode.right = right
        newNode.left = left
        pq.put(newNode)

    # root stores pointer to root of Huffman Tree
    root = pq.queue[0]
    
    # traverse the Huffman tree and store the Huffman codes in a map
    huffmanCode = {}
    encode(root, "", huffmanCode)

    # print the Huffman codes
    print(f"Original Keys: {symbolProbs.keys()}")
    print(f"Huff keys: {huffmanCode.keys()}")
    print("Huffman Codes are :")
    print(huffmanCode)
    # for entry in symbolProbs:
    #     print(f"{entry} {huffmanCode[entry]}")
    return huffmanCode

print("Quantizing red band...")
newRBand = quantizeBand(rBand)
print("Quantizing blue band...")
newBBand = quantizeBand(bBand)
print("Quantizing green band...")
newGBand = quantizeBand(gBand)

print("Calculating symbol probabilities for red band...")
rSymbolProbs = gatherSymbolProbs(newRBand)
print("Calculating symbol probabilities for blue band...")
bSymbolProbs = gatherSymbolProbs(newBBand)
print("Calculating symbol probabilities for green band...")
gSymbolProbs = gatherSymbolProbs(newGBand)


print("Calculating Huffman codenames for red band...")
rHuffmanCode = buildHuffmanTree(rSymbolProbs)

print("Encoding RBand...")
encodedRBand = []
for pixel in newRBand:
    encodedRBand.append(huffmanCode[pixel])

bitstream = bitarray.bitarray(''.join(encodedRBand))

with open('tux.data', 'wb') as f:
    f.write(bitstream)

# if __name__ == "__main__":
#     text = "Huffman coding is a data compression algorithm.";
# 	buildHuffmanTree(text);