import argparse
from pprint import pprint as pp

def calculate_epic(dot):
	if dot == 0:
		return 0
	number_line = [_ for _ in range(0, dot + 1)]
	auto_successes = 0
	success_list = {}
	epic_attr = 0
	for n in number_line:
		if len(success_list) > 1:
			epic_attr = (n-1) + success_list[str(n-1)]
			success_list[str(n)] = epic_attr
		else:
			success_list[str(n)] = 1
	
	return success_list[str(dot)]

def calculate_epic_as_dict(dot):
	if dot == 0:
		return 0
	number_line = [_ for _ in range(0, dot + 1)]
	auto_successes = 0
	success_list = {}
	epic_attr = 0
	for n in number_line:
		if len(success_list) > 1:
			epic_attr = (n-1) + success_list[str(n-1)]
			success_list[str(n)] = epic_attr
		else:
			success_list[str(n)] = 1
	
	return success_list
	
if __name__ == "__main__":
	  
	parser = argparse.ArgumentParser(description="Automatic Success calculator for Scion 1e.")
	parser.add_argument('--calc','-c', type=int)

	args = parser.parse_args()

	if args.calc > 0:
		print(f"{args.calc} dots in an epic attribute grant: {calculate_epic(args.calc)} automatic successes!")
	else:
		for _ in range(0,25):
			print(f"{_} dots in an epic attribute grant: {calculate_epic(_)} automatic successes!")
