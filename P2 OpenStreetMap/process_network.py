__author__ = 'kanhua'

import re

def parse_network_str(input_str):

    assert isinstance(input_str,str)
    input_str_lst=input_str.split(";")

    new_str_list=[s.strip() for s in input_str_lst]

    return new_str_list


def test_parse_network_str():

    assert parse_network_str("London Underground")==["London Underground"]
    assert parse_network_str("London Underground; British Rail")==["London Underground","British Rail"]


def extract_area(postcode_str):

    reg_str="(?P<area>^(E|EC|N|NW|SE|SW|W|WC|WD|HA|UB|TW|KT|SM|CR|BR|DA|RM|IG|CM|EN)[0-9][0-9]*)\s*[0-9][A-Z][A-Z]"
    prog=re.compile(reg_str)
    match_group=prog.match(postcode_str)
    if match_group is None:
        return "NA"
    else:
        return match_group.group("area")


def validate_uk_postcodes(postcode_str):

    assert isinstance(postcode_str,str)
    # Verify the second part

    postcode_str=postcode_str.strip()
    postcode_str=postcode_str.upper()
    unit_code=postcode_str[-3:]
    area_code=postcode_str[:-3].rstrip()


    if validate_area_code(area_code) and validate_unit_code(unit_code):
        return area_code,unit_code
    else:
        return "NA","NA"


def validate_area_code(area_code_str):

    assert isinstance(area_code_str,str)

    #AA9A
    #reg_str="(WC postcode area; EC1–EC4, NW1W, SE1P, SW1)"
    reg_aa9a_str="(WC[0-9][A-Z])|(EC[1234][A-Z])|(NW1W)|(SE1P)|(SW1[A-Z])"

    #A9A
    #E1W, N1C, N1P

    reg_a9a_str="(W1[ABCDEFGHJKPSTUW])|(E1W)|(N1C)|(N1P)"

    #A9 or A99
    # B, E, G, L, M, N, S, W

    reg_a9_str="([BEGLMNSW][0-9][0-9]*)"

    # AA9 or AA99
    # all other postcodes

    # QVX is excluded in the first position
    # IJZ is excluded in the second position
    reg_aa9_str="([ABCDEFGHIJKLMNOPRSTUWYZ][ABCDEFGHKLMNOPQRSTUVWXY][0-9][0-9]*)"


    reg_area_code=(reg_aa9a_str+'|'+reg_a9a_str+'|'+reg_a9_str+"|"+reg_aa9_str)

    match_result=re.fullmatch(reg_area_code,area_code_str)
    if match_result:
        return True

    return False

def validate_unit_code(unit_code_str):

    assert isinstance(unit_code_str,str)

    unit_pat="[0-9][A-Z][A-Z]"

    match_result=re.fullmatch(unit_pat,unit_code_str)

    if match_result:
        return True
    else:
        return False


def test_validate_area_code():

    assert validate_area_code("WC1A")==True

    assert validate_area_code("238E")==False

    assert validate_area_code("WC9Z")==True
    assert validate_area_code("W2J")==False

    assert validate_area_code("EC25")==True
    assert validate_area_code("WC22")==True

    assert validate_area_code("QI5")==False


def test_validate_UK_postcode():

    assert validate_uk_postcodes("kt32gz")==("KT3","2GZ")
    assert validate_uk_postcodes("wc2n4ty")==("WC2N","4TY")

    assert validate_uk_postcodes("kt32")==("NA","NA")
    assert validate_uk_postcodes("k")==("NA","NA")

def test_extract_area():
    assert extract_area("SW19 2HQ")=="SW19"
    assert extract_area("KT3 2GZ")=="KT3"

if __name__=="__main__":


    test_parse_network_str()

    test_extract_area()

    #print(validate_uk_postcodes("WC1B 5HR"))

    test_validate_area_code()

    test_validate_UK_postcode()


