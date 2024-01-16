# test_main.py

import subprocess
import json
from decimal import Decimal

TEST = 3

def test_main(i,input_file, window_size, expected_output_file):
    output = subprocess.check_output(["python3", "unbabel_cli.py", "--input_file", input_file, "--window_size", str(window_size)], text=True)

    with open(expected_output_file, "r") as file:
        expected_content = json.load(file)

    if json.loads(output.replace("'", "\""), parse_float=Decimal) == expected_content:
        print ("Test #" + str(i) + " passed")
    else:
        print ("Test #" + str(i) + " failed")


for i in range(1,TEST + 1):
    test_main(i,"inputs/"+str(i)+".json", 10, "expected_outputs/"+str(i)+".json")
