
def is_valid(ipv4):
    """ check if valid ipv4 format """
    try:
        ipv4 = ipv4.split('.')
        if len(ipv4) != 4:
            return False
        if any(len(i) > 3 for i in ipv4):
            return False
        for i in ipv4:
            if (int(i) < 0) or (int(i) > 255):
                return False
        return True
    except:
        return False


def ip_to_num(ipv4):
    """ convert ipv4 to integer """
    ipv4 = ipv4.split('.')
    ipv4 = [int(i) for i in ipv4]
    ipv4 = ipv4[3] | (ipv4[2] << 8) | (ipv4[1] << 16) | (ipv4[0] << 24)
    return ipv4
