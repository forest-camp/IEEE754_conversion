import sys


def print_sign(x):
    if x == "0":
        return "0"
    else:
        return "1"


def convert_exp_to_int(x):
    tmp = 0.0
    for i in range(len(x)):
        tmp += int(x[i]) * (2**(7-i))
    return int(tmp) - 127, int(tmp)


def convert_man_to_float(x, is_denorm=False):
    tmp = 0
    res = 0.0
    if is_denorm:
        for i in range(len(x)):
            tmp += int(x[i]) * (2 ** (22 - i))
        res = tmp / (2**22)
    else:
        x = "1" + x
        for i in range(len(x)):
            tmp += int(x[i]) * (2**(23 - i))
        res = tmp / (2 ** 23)
    return res, int(tmp) % 8388608


def convert(x):
    assert(x <= 0xffffffff)
    x = x + 0x100000000
    sign = bin(x)[3]
    exp = bin(x)[4: 4 + 8]
    man = bin(x)[4 + 8:]
    is_denorm = (exp == "0" * 8) & (man != "0" * 23)
    is_inf = (exp == "1" * 8) & (man == "0" * 23)
    is_nan = (exp == "1" * 8) & (man != "0" * 23)

    exp_f, exp_i = convert_exp_to_int(exp)
    man_f, man_i = convert_man_to_float(man, is_denorm)

    print(" " * 31, "SIGN".center(5), "\t", "EXP".center(20), "\t", "MAN".center(50))
    print("Value".ljust(30), ":", print_sign(sign).center(5), "\t", str(exp_f).center(20), "\t", str(man_f).center(50))
    print("Encoded as".ljust(30), ":", print_sign(sign).center(5), "\t", str(exp_i).center(20), "\t", str(man_i).center(50))
    print("Binary".ljust(30), ":", print_sign(sign).center(5), "\t", exp.replace('', ' ').center(20), "\t", man.replace('', ' ').center(50))
    res = (-1 ** int(sign)) * man_f * (2 ** exp_f)
    print("Decimal representation".ljust(30), ":", str(res))
    print("Binary Representation".ljust(30), ":", str(bin(x)[:2] + bin(x)[3:]))
    print("Hexadecimal Representation".ljust(30), ":", str(hex(x)[:2] + hex(x)[3:]))
    if is_denorm:
        print('*' * 110)
        print('DENORM!'.center(110))
        print('*' * 110)
    if is_inf:
        print('*' * 110)
        print('INFINITE!'.center(110))
        print('*' * 110)
    if is_nan:
        print('*' * 110)
        print('Not a Number!'.center(110))
        print('*' * 110)


if __name__ == "__main__":
    if sys.argv[1][:2] == "0x":
        convert(int(sys.argv[1], 16))
    elif sys.argv[1][:2] == "0b":
        convert(int(sys.argv[1], 2))
    else:
        print("Not supported type!")
