import argparse
parser=argparse.ArgumentParser()
parser.add_argument("square", help="display a square of a number", type=int)
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
args=parser.parse_args()


#print(args.square**2)

answer=args.square**2

if args.verbose:
	#print(f"the square of {args.square} equals {answer}")
	print("the squre of %d equals %d" %(args.square, answer))
else:
	print(answer)
	
