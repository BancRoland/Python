import argparse
parser=argparse.ArgumentParser()
parser.add_argument("square", 
	help="display a square of a number", type=int)
#parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
parser.add_argument("-v", "--verbose", action="count", default=0,
	help="increase output verbosity") 
args=parser.parse_args()


#print(args.square**2)

answer=args.square**2

if args.verbose>=2:
	print(f"the square of {args.square} equals {answer}")
	#print("the squre of %d equals %d" %(args.square, answer))
elif args.verbose>=1:
	print(f"{args.square}^2 = {answer}");
	
else:
	print(answer)
	
	
#python3 parsarg3.py 4 -vv

