import argparse

parser = argparse.ArgumentParser(description="calculate the area of circle with radius r")

parser.add_argument("-r","--radius", help="radius of the circle", nargs='?', type=float, const=1, default=7, required=True)
parser.add_argument("-pi","--pi", help="the ratio called pi", nargs='?', type=float, const=1, default=3.14159)

args=parser.parse_args()
answer=args.radius**2*args.pi

print(answer)
    
