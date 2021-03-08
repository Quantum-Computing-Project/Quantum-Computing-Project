"""
All other functions that might be used in the code are contained in this module.
"""


def binary_to_decimal(binary):
    return int(str(binary), 2)


def decimal_to_binary(decimal):
    return bin(decimal).replace("0b", "")


if __name__ == "__main__":
    print(binary_to_decimal(1010))
    print(decimal_to_binary(20))
