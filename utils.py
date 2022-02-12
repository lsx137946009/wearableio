# -*- coding: utf-8 -*-


def join_integer_decimal(block) -> float:
    integer = block[0]
    decimal = block[1]
    decimal = decimal / 100
    parsed = integer + decimal
    return parsed


def join_byteblocks(block, reverse=False) -> int:
    """
    join_byteblocks used to combine low bit data and high bit data

    Parameters
    ----------
    block : list
        Low Digit Block -> int
        High Digit Block -> int

    Returns
    -------
    parsed : int
        low | high << 8 ...

    Example:
        LowDigitBlock = 0     # 0xff
        HighDigitBlock = 255  # 0x00
        block = [LowDigitBlock, HighDigitBlock] # low first
        join_byteblocks(block)
        -> 65280              # 0xff00
    """
    if reverse:
        block.reverse()
    parsed = 0
    for key, val in enumerate(block):
        parsed = parsed | val << 8 * key
    return parsed


def join_complementary_byteblocks(block) -> int:
    """
    join_complementary_byteblocks used to combine low bit data and high bit data
    as the representation of complementary code

    Parameters
    ----------
    block : list
        Low Digit Block -> int
        High Digit Block -> int

    Returns
    -------
    parsed : int
        low | high << 8 ... (complementary code)

    Example:
        LowDigitBlock = 0     # 0xff
        HighDigitBlock = 255  # 0x00
        block = [LowDigitBlock, HighDigitBlock] # low first
        join_complementary_byteblocks(block)
        -> -256               # -0x100

    """
    n_byte = len(block)
    sign_bound = 2 ** (n_byte * 8 - 1)
    sign_block = 2 ** (n_byte * 8)
    parsed = join_byteblocks(block)
    if parsed < sign_bound:
        return parsed
    else:
        return parsed - sign_block