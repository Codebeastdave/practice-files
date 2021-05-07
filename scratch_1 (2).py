#

class Calc:
    def __init__(self, x, y, operator):
        self.minus = "-"
        self.plus = "+"
        self.x = x
        self.y = y
        self.operator = operator

    def add(self):
        assert self.operator == self.plus
        results = str(self.x) + self.operator + str(self.y)
        return "{0} = {1}\n".format(results, eval(results))

    def subtract(self):
        assert self.operator == self.minus
        results = str(self.x) + self.operator + str(self.y)
        return "{0} = {1}\n".format(results, eval(results))


class ProcessCalc:
    def __init__(self):
        self.filename = input("filename: ")
        self.calculations = int(input("number of calculations: "))
        self.__input_x = ""
        self.__input_y = ""
        self.__operator = ""

    def store(self):
        x = open(r"C:\Users\DAVID\.PyCharmCE2019.1\config\scratches\{0}".format(self.filename), "w")
        x.close()
        x = open(r"C:\Users\DAVID\.PyCharmCE2019.1\config\scratches\{0}".format(self.filename), "r")
        if x.read():
            x.close()
            x = open(r"C:\Users\DAVID\.PyCharmCE2019.1\config\scratches\{0}".format(self.filename), "a")
            print("false")
        else:
            x.close()
            x = open(r"C:\Users\DAVID\.PyCharmCE2019.1\config\scratches\{0}".format(self.filename),
                     "w")
            print("falser")

        for loop in range(self.calculations):
            self.__input_x = input("x: ")
            self.__input_y = input("Y: ")
            self.__operator = input("operator")
            if self.__operator == "+":
                x.write(Calc(self.__input_x, self.__input_y, self.__operator).add())
            else:
                x.write(Calc(self.__input_x, self.__input_y, self.__operator).subtract())
        x.close()


ProcessCalc().store()

