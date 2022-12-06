# 正常版
import base64
# md5加密
import hashlib


# MD5加密
def md5_encrypt(src: str):
    hl = hashlib.md5()
    hl.update(src.encode(encoding='gb2312'))
    return hl.hexdigest()


# MD5解密
def md5decrypt(num: str):
    with open('./module/md5.txt', 'r') as f:
        result = 0
        for line in f:
            line = line.split('\n')
            if num == line[0]:
                return result
            else:
                result += 1
        return None


# 解密
def dekey(code: str):
    key = str(code[:4] + code[8:])
    res = base64.b64decode(key)
    return res.decode()


# 用户登录解密
def user_login_de_base(password: str):
    password = base64.b64decode(password).decode()[:-7]
    return password


# 密码加密
def jiami(zifu):
    m = hashlib.md5()
    m.update(zifu.encode("utf8"))
    a = m.hexdigest()
    a2 = a[0:30]
    b = 'a'
    c = 'b'
    lie1 = list(a2)
    lie1.insert(5, b)
    a3 = ''.join(lie1)
    lie2 = list(a3)
    lie2.insert(10, c)
    a4 = ''.join(lie2)
    return a4


if __name__ == '__main__':
    print(user_login_de_base("d3p4MTk5NDYyOTE2NjkwODQ4NDc2OTkwMjE4"))
