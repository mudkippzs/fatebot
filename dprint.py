import argparse
import pprint
import datetime

def dprint(message:[list, dict, str, int, bool] = None, debug_identifier:str = "Err: No Identifier set"):
	now = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S:")
	base_message = f"\n[DEBUG]@[ {now}]>[{debug_identifier}])\n"
	message = str(message)

	if type(message) in ["list", "dict"]:
		print(base_message)
		pp(message)
	else:
		print(base_message + "\t" + message)

if __name__ == "__main__":
	dprint("Debugger Printer Module Test Message.", "Test")
