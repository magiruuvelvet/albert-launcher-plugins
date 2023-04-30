from typing import Optional;

def kanji2dec(number_with_kanji: str) -> Optional[float]:
    """
    Normalizes the given number with kanji to a decimal number.

    Args:
      number_with_kanji: number with kanji

    Returns:
      normalized number or None if the input is unsupported
    """

    # normalized number
    number = None;

    # multiplication factor
    multiply_by = 1;

    # basic single character checks
    if number_with_kanji == "一":
        return 1;
    elif number_with_kanji == "二":
        return 2;
    elif number_with_kanji == "三":
        return 3;
    elif number_with_kanji == "四":
        return 4;
    elif number_with_kanji == "五":
        return 5;
    elif number_with_kanji == "六":
        return 6;
    elif number_with_kanji == "七":
        return 7;
    elif number_with_kanji == "八":
        return 8;
    elif number_with_kanji == "九":
        return 9;
    elif number_with_kanji == "十":
        return 10;
    elif number_with_kanji == "百":
        return 100;
    elif number_with_kanji == "千":
        return 1000;
    elif number_with_kanji == "万":
        return 10000;

    # more advanced checks and conversions

    # if number ends with 万 multiply by 10000 (1万=10000)
    if number_with_kanji.endswith("万"):
        number = float(number_with_kanji[:-1]);
        multiply_by = 10000;

    if number != None:
        return number * multiply_by;
    else:
        return None;

# embedded tests (generated with Tabnine)
if __name__ == "__main__":
    # single character tests
    assert kanji2dec("一") == 1;
    assert kanji2dec("二") == 2;
    assert kanji2dec("三") == 3;
    assert kanji2dec("四") == 4;
    assert kanji2dec("五") == 5;
    assert kanji2dec("六") == 6;
    assert kanji2dec("七") == 7;
    assert kanji2dec("八") == 8;
    assert kanji2dec("九") == 9;
    assert kanji2dec("十") == 10;
    assert kanji2dec("百") == 100;
    assert kanji2dec("千") == 1000;
    assert kanji2dec("万") == 10000;

    # more advanced tests
    assert kanji2dec("1万") == 10000;
    assert kanji2dec("2万") == 20000;
    assert kanji2dec("3万") == 30000;
    assert kanji2dec("4万") == 40000;
    assert kanji2dec("5万") == 50000;
    assert kanji2dec("6万") == 60000;
    assert kanji2dec("7万") == 70000;
    assert kanji2dec("8万") == 80000;
    assert kanji2dec("9万") == 90000;
    assert kanji2dec("10万") == 100000;
    assert kanji2dec("10.1万") == 101000;
    assert kanji2dec("12.4万") == 124000;
    assert kanji2dec("11万") == 110000;
    assert kanji2dec("12万") == 120000;
    assert kanji2dec("13万") == 130000;
    assert kanji2dec("14万") == 140000;
    assert kanji2dec("15万") == 150000;
    assert kanji2dec("16万") == 160000;
    assert kanji2dec("17万") == 170000;
    assert kanji2dec("18万") == 180000;
    assert kanji2dec("19万") == 190000;
    assert kanji2dec("20万") == 200000;
    assert kanji2dec("100万") == 1000000;
    assert kanji2dec("110万") == 1100000;
    assert kanji2dec("101万") == 1010000;
    assert kanji2dec("200万") == 2000000;
    assert kanji2dec("1000万") == 10000000;
    assert kanji2dec("2000万") == 20000000;

    # test for invalid input
    assert kanji2dec("") == None;
