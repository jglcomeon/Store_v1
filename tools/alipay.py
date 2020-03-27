
from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from urllib.parse import quote_plus
from base64 import decodebytes, encodebytes
import json
class AliPay(object):
  """
  支付宝支付接口(PC端支付接口)
  """
  def __init__(self, appid, app_notify_url, app_private_key_path,
         alipay_public_key_path, return_url, debug=False):
    self.appid = appid
    self.app_notify_url = app_notify_url
    self.app_private_key_path = app_private_key_path
    self.app_private_key = None
    self.return_url = return_url
    #self.app_private_key = RSA.import_key('-----BEGIN PUBLIC KEY-----\nMIIEogIBAAKCAQEAmYdMYrlczIR7Mw/5GLWXn1Cpm0rt7F2dBFqYzkQzid5XE1mBDMNuXWL6n9/Ok8JwVdb+xXNBA3hm+VdkVSSHSk39oECcRvLBpUe48V75O4++R87s/60ecfmtJjgtbE40brssoRGcxwwPHixcrHlJRtOMS3U8s7de5+zl3Kc+Rfjri7du0h8/LuUWr5oOPNuLE1pv7QhYUucaIXO+nz7BW4IjsHtpFdKP2aUZzWaQ/U7oOuvldtUTfkTNsKzCvjp2U2Nxmf47wKXYjbTPvOCzEMlU+yjbHm8pO+hnNpV3AeJaWCLy+l1v6jKkkkJ21lk0CALd3J3HgRQaFBL1Jtg+lQIDAQABAoIBAB7Iz1s4WdA0fFOXz1XSC64JSYj29FAh0TsvQ1aQvFjXuVQK7WJ2yWl2UFTAVrawFUBRFNLYsl+Uw+kZSef8pBgVHVcFvZBIWuXeRMo5RfZYc0oIxuLZfrJR4xM3znvaDo9pfqBpXKtY0qs1L/vxcez+vDHhNyO+EAynJswgyM7UswG2wyMIamq5t7jfiYuVU8eJFyXzodgEOE5iZrddKtmQEZ3PgO1KBbb0yBgzmn756QrWkS7vX7WXRHUVvSS3SbUpNQyysgu3Pi5DnadbJ5QOa2dWcujxo9pVDvvENfwsmpD+8hwON+Ovrs7khXxECCBTrU/dPs0pqDB0V4e1Jv0CgYEA7FxBSzrO0VUMtir6OQwDOH2kK6G5OoTGsB5o45cv7xP4Paefd1cCux4w3lycTq077o1DVBAFkgrFDrEwoWIMn4PFXbfluOx5g6fQPn95FC+v6AsYDUSQfQPHe9pShQ9McG0MjB5+gRy+PlBmRCrWsnALXcs0ahukoHXLp1826IcCgYEApkkVYTaoeXp2q8f8ETWezr1vsXcHWjQC1ezIA6dqM+J0CZIAzrj38Tu/DspZpSrqeVKmmZfkUX1WXhK1dV9xhwIONM7VgFjBXQf9E3iShOM0DBA7To3xDBr3nQzVaIBlWkXq4RAwwRAghifsq+eKSn6MQ6qUdp2/Alp0bBJikwMCgYBDqXFDoPUdtdQqvgjdldPCMy1xFB3bY7EhL8NlC528OiJBPCAJYM42VME2lppkZ3EVrDjO8rs1gIHC3/SE7nWgoG86ke9gTcnHZ53UlldJ8RDRQ4PCIJOgRhmwGeKvlp6SPJVv8zbRrTHE0u1DrGPDtxF56zb4/SrWiIIhSr+ENwKBgEtRrTp0XIlxvBEBK57L79vrGI2EwbLM/j/R2aM2ELfhqfevx2fbhoshKeBULZjPwJclpcrKbyOuJxHDXagFjFG/z5mB2lkhWqx98tb/9TX2B9wy+foR9w4ppODhMET+a2ohY0uAXuUEHgdGTEBtR0mI2pXHzSmRODSjrjpJdZbrAoGAR1ra1BQ8IOFjYETHyK+D3KT1iniMol4+GtDJxj7/+Ra/wsJ/SxEba/dZvb8cywopbYTqtH19LbYYHYm+TFX1s64ZisCOfutiQ1rOW7t3j1JYML2MtItLeJ5Wiygm7bgX993v8cLP8XkDk2Wuf7+R38JEK+7P7tDUKDA2wrzH+/A=\n-----END PUBLIC KEY-----')
    #self.alipay_public_key = RSA.importKey('-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvzdf2NBmntjzH+fTyZiKbX9CScfQ3blmJ3FmDRiNtxvVIgjwNGMk3bRG1YPsiQ/HhMAZydibh1PeMt/VBMZs0/O8qVTqSnUb22hS71rX/M3R93N5GOJu435vwBE8DXHmlV4f62Kz12tNVnLi9UuGacdK0N3s2xOjKmA3tkcrJXDxC3NXJVZJIuq+F/d6gZly6LK636wR5gdjylturP7NlYmabDIZgVAmtAm6sksdtMUm2R7Ebb0AtzjgrM74D+0Hgas6xEPHbvq0mIM9ImhvwbTPcv8X3dFZNxbK6/R7NOAFUI8taYY6ofi7SXl/yirxAR+CR7DvjSPBlfJoM1+WbQIDAQAB\n-----END PUBLIC KEY-----')
    with open(self.app_private_key_path) as fp:
      self.app_private_key = RSA.importKey(fp.read())
      self.app_private_key
    self.alipay_public_key_path = alipay_public_key_path
    with open(self.alipay_public_key_path) as fp:
      self.alipay_public_key = RSA.importKey(fp.read())
    if debug is True:
      self.__gateway = "https://openapi.alipaydev.com/gateway.do"
    else:
      self.__gateway = "https://openapi.alipay.com/gateway.do"
  def direct_pay(self, subject, out_trade_no, total_amount, return_url=None, **kwargs):
    biz_content = {
      "subject": subject,
      "out_trade_no": out_trade_no,
      "total_amount": total_amount,
      "product_code": "FAST_INSTANT_TRADE_PAY",
      # "qr_pay_mode":4
    }
    biz_content.update(kwargs)
    data = self.build_body("alipay.trade.page.pay", biz_content, self.return_url)
    return self.sign_data(data)
  def build_body(self, method, biz_content, return_url=None):
    data = {
      "app_id": self.appid,
      "method": method,
      "charset": "utf-8",
      "sign_type": "RSA2",
      "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
      "version": "1.0",
      "biz_content": biz_content
    }
    if return_url is not None:
      data["notify_url"] = self.app_notify_url
      data["return_url"] = self.return_url
    return data
  def sign_data(self, data):
    data.pop("sign", None)
    # 排序后的字符串
    unsigned_items = self.ordered_data(data)
    unsigned_string = "&".join("{0}={1}".format(k, v) for k, v in unsigned_items)
    sign = self.sign(unsigned_string.encode("utf-8"))
    # ordered_items = self.ordered_data(data)
    quoted_string = "&".join("{0}={1}".format(k, quote_plus(v)) for k, v in unsigned_items)
    # 获得最终的订单信息字符串
    signed_string = quoted_string + "&sign=" + quote_plus(sign)
    return signed_string
  def ordered_data(self, data):
    complex_keys = []
    for key, value in data.items():
      if isinstance(value, dict):
        complex_keys.append(key)
    # 将字典类型的数据dump出来
    for key in complex_keys:
      data[key] = json.dumps(data[key], separators=(',', ':'))
    return sorted([(k, v) for k, v in data.items()])
  def sign(self, unsigned_string):
    # 开始计算签名
    key = self.app_private_key
    signer = PKCS1_v1_5.new(key)
    signature = signer.sign(SHA256.new(unsigned_string))
    # base64 编码，转换为unicode表示并移除回车
    sign = encodebytes(signature).decode("utf8").replace("\n", "")
    return sign
  def _verify(self, raw_content, signature):
    # 开始计算签名
    key = self.alipay_public_key
    signer = PKCS1_v1_5.new(key)
    digest = SHA256.new()
    digest.update(raw_content.encode("utf8"))
    if signer.verify(digest, decodebytes(signature.encode("utf8"))):
      return True
    return False
  def verify(self, data, signature):
    if "sign_type" in data:
      sign_type = data.pop("sign_type")
    # 排序后的字符串
    unsigned_items = self.ordered_data(data)
    message = "&".join(u"{}={}".format(k, v) for k, v in unsigned_items)
    return self._verify(message, signature)