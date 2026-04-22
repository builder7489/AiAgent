from functions.run_python_file import run_python_file

working_dir = "calculator"

test_a = {
    "name": "Test A",
    "filepath": "main.py",
    "args": 0
}

test_b = {
    "name": "Test B",
    "filepath": "main.py",
    "args": ["3 + 5"]
}

test_c = {
    "name": "Test C",
    "filepath": "tests.py",
    "args": 0
}

test_d = {
    "name": "Test D",
    "filepath": "../main.py",
    "args": 0
}

test_e = {
    "name": "Test E",
    "filepath": "nonexistent.py",
    "args": 0
}

test_f = {
    "name": "Test F",
    "filepath": "lorem.txt",
    "args": 0
}

testing_run = [test_a, test_b, test_c, test_d, test_e, test_f]

for test in testing_run:
    if test["args"] == 0:
        print(f"\n---")
        print(test["name"])
        print(run_python_file(working_dir, test["filepath"]))
        print(f"---\n")
    else:
        print(f"\n---")
        print(test["name"])
        print(run_python_file(working_dir, test["filepath"], test["args"]))
        print(f"---\n")