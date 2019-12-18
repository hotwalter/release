class Human:
    def __init__(self,name):
        self.name = name

    def __enter__(self):
        print("执行Enter")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("执行exit方法")
        print(exc_tb,exc_val,exc_tb)
        return False

    def __getattr__(self, item):
        print("执行getattr")
        print(item)
        self.__dict__[item] = "nan"




with Human("xiaoming") as f:
    print(f.sex)
    print(f.sex)
    # print(;;;)
    print(f.sex)