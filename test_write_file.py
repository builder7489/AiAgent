from functions.write_file import write_file

# TODO set working directory
test_dir = "calculator"

# TODO set file paths to test
test_a = {
    "name": "Test A",
    "filepath": "lorem.txt",
    "content": "wait, this isn't lorem ipsum"
}

test_b = {
    "name": "Test B",
    "filepath": "pkg/morelorem.txt",
    "content": "lorem ipsum dolor sit amet"
}

test_c = {
    "name": "Test C",
    "filepath": "/tmp/temp.txt",
    "content": "this should not be allowed"
}

test_filepaths = [test_a, test_b, test_c]

# TODO build running test display
for test in test_filepaths:
    print(f"\n---")
    print(test["name"])
    print(write_file(test_dir, test["filepath"], test["content"]))
    print(f"---\n")