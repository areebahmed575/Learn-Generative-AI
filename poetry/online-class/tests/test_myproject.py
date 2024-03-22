from online_class import main


def test_function1():
    r = main.my_function()
    assert r == "Hello World"


def test_function2():
    r = main.my_function()
    assert r != "Pakistan"



#poetry run pytest --> for run