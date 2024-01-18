def func(x):
    return x + 1


def test_answer():
    assert func(3) == 5
# for individual run pytest test_class.py
# if you want not to get additional information pytest -q test_class.py
# pytest will run all files of the form test_*.py or *_test.py in the current directory and its subdirectories. More generally, it follows    
