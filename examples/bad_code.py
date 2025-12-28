def process(data):
    result = []
    for i in range(len(data)):
        if data[i] > 0:
            if data[i] % 2 == 0:
                if data[i] < 100:
                    result.append(data[i] * 2)
                else:
                    result.append(data[i])
            else:
                if data[i] < 50:
                    result.append(data[i] + 1)
                else:
                    result.append(data[i] - 1)
        else:
            result.append(0)
    return result

def x(a,b,c,d,e,f,g):
    return a+b+c+d+e+f+g

class MyClass:
    def method1(self,x,y,z,a,b,c):
        if x > y:
            if y > z:
                if z > a:
                    if a > b:
                        if b > c:
                            return x
        return c