import sys
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import rsa


class prpcrypt():
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC

    # 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)

        length = 16
        count = len(text)
        if (count % length != 0):
            add = length - (count % length)
        else:
            add = 0
        text = text + ('\0' * add).encode()
        self.ciphertext = cryptor.encrypt(text)
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip(('\0').encode())


def encryption_file(filedata):
    with open('./static/secret/publickey.txt', 'rb') as f:  # 以二进制写类型打开
        publicKey = (f.read()).decode()

        # 将获取得到的字符串转化为公钥所需参数(n,e)
        para1 = publicKey[10:-8]
        para2 = publicKey[-6:-1]

        # 公钥初始化
        publicKey = rsa.key.PublicKey(int(para1), int(para2))

    with open('./static/secret/privatekey.txt', 'rb') as f:  # 以二进制写类型打开
        privateKey = (f.read()).decode()

        # 解析字符串转换为私钥所需的五个参数（n,e,d,p,q）
        para3 = privateKey[len(para1) + len(para2) + 15:-1]
        para4 = para3[:-908]
        para3 = para3[-906:]
        para3, para4 = para4, para3
        para5 = para4[:480]
        para4 = para4[482:]
        para4, para5 = para5, para4

        # 私钥初始化
        privateKey = rsa.key.PrivateKey(int(para1), int(para2), int(para3), int(para4), int(para5))

    # 获得对称密钥
    with open('./static/secret/symmetrickey.txt', 'rb') as f:  # 以二进制写类型打开
        secretkey = f.read()
        message = rsa.decrypt(secretkey, privateKey)

    # 采用AES_CBC模式加密
    secretkey = message
    pc = prpcrypt(secretkey)  # 初始化密钥

    # 加密操作
    return pc.encrypt(filedata)

    # file = open('E:/大学/大二下/更新操作.PNG', 'rb').read()
    # e = pc.encrypt(file)
    # with open('E:/大学/大二下/1.PNG', 'wb') as f:  # 以二进制写类型打开
    #     f.write(e)  # 写入文件

    # # 解密操作
    # file = open('E:/大学/大二下/1.PNG', 'rb').read()
    # d = pc.decrypt(file)
    # with open('E:/大学/大二下/2.PNG', 'wb') as f:  # 以二进制写类型打开
    #     f.write(d)  # 写入文件

