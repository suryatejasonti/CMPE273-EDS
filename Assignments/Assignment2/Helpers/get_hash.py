from hashlib import md5

def hashit(val):
        m = md5(val.encode())
        return int(m.hexdigest(), 16)