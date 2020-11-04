import sys


def print_sign(x):
    if x == "0":
        return "0"
    else:
        return "1"


def convert_exp_to_int(x):
    tmp = 0.0
    for i in range(len(x)):
        tmp += int(x[i]) * (2**(4-i))
    return int(tmp) - 15, int(tmp)


def convert_man_to_float(x, is_denorm=False):
    tmp = 0
    res = 0.0
    if is_denorm:
        for i in range(len(x)):
            tmp += int(x[i]) * (2 ** (9 - i))
        res = tmp / (2**9)
    else:
        x = "1" + x
        for i in range(len(x)):
            tmp += int(x[i]) * (2**(10 - i))
        res = tmp / (2 ** 10)
    return res, int(tmp) % 1024


def convert(x):
    assert(x <= 0xffff)
    x = x + 0x10000
    sign = bin(x)[3]
    exp = bin(x)[4: 4 + 5]
    man = bin(x)[4 + 5:]
    is_denorm = (exp == "0" * 5) & (man != "0" * 10)
    is_inf = (exp == "1" * 5) & (man == "0" * 10)
    is_nan = (exp == "1" * 5) & (man != "0" * 10)

    exp_f, exp_i = convert_exp_to_int(exp)
    man_f, man_i = convert_man_to_float(man, is_denorm)

    print(" " * 30, "SIGN".center(5), "\t", "EXP".center(15), "\t", "MAN".center(25))
    print("Value :".ljust(30), print_sign(sign).center(5), "\t", str(exp_f).center(15), "\t", str(man_f).center(25))
    print("Encoded as :".ljust(30), print_sign(sign).center(5), "\t", str(exp_i).center(15), "\t", str(man_i).center(25))
    print("Binary :".ljust(30), print_sign(sign).center(5), "\t", exp.replace('', ' ').center(15), "\t", man.replace('', ' ').center(25))
    res = (-1 ** int(sign)) * man_f * (2 ** exp_f)
    print("Decimal representation:".ljust(30), str(res))
    print("Binary Representation:".ljust(30), str(bin(x)[:2] + bin(x)[3:]))
    print("Hexadecimal Representation:".ljust(30), str(hex(x)[:2] + hex(x)[3:]))
    if is_denorm:
        print('*' * 80)
        print('DENORM!'.center(80))
        print('*' * 80)
    if is_inf:
        print('*' * 80)
        print('INFINITE!'.center(80))
        print('*' * 80)
    if is_nan:
        print('*' * 80)
        print('Not a Number!'.center(80))
        print('*' * 80)


if __name__ == "__main__":
        if sys.argv[1][:2] == "0x":
        convert(int(sys.argv[1], 16))
    elif sys.argv[1][:2] == "0b":
        convert(int(sys.argv[1], 2))
    else:
        print("Not supported type!")
