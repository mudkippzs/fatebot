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
	# print(calculate_epic(0)) # 0
	# print(calculate_epic(1)) # 1
	# print(calculate_epic(2)) # 2
	# print(calculate_epic(6)) # 16
	# print(calculate_epic(15)) # 22
	# print(calculate_epic(32)) # 497
	pp(calculate_epic_as_dict(10000001))

