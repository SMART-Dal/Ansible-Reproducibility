from math import sqrt


def calculate_phi(a,b,c,d):
    up = (a*d) - (c*b)
    down = sqrt((a+b)*(c+d)*(a+c)*(b+d))
    return up/down


if __name__ == '__main__':

    print(str(calculate_phi(28,12227,4085,19598)))