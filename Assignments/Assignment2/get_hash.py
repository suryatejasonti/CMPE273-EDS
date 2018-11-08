from hashlib import md5

def hash(val):
        m = md5(val.encode())
        return int(m.hexdigest(), 16)