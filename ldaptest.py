from ldap3 import Server, Connection, ALL,SUBTREE

# if __name__ == "__main__":
def check_valid(username,password):
    if username=="admin" and password=="admin":
        return True
    else:
        return False
    # host为域控服务器ip
    # host = 'ad03.aibee.cn'
    # username = 'yhwang'
    # try:
    #     server = Server(host, use_ssl=True, get_info=ALL)
    #     # user（如domain\Administrator）和passwod为登录域控服务器的账户密码
    #     conn = Connection(server, 'cn=DataAlart,ou=project-account,ou=aibee,dc=aibee,dc=cn', 'Data_platform',check_names=True, lazy=False, raise_exceptions=False)
    #     conn.open()
    #     conn.bind()
    #     res = conn.search('OU=aibee,DC=aibee,DC=cn',attributes=['cn', 'givenName', 'mail', 'sAMAccountName'],search_filter = '(sAMAccountName={})'.format(username),search_scope = SUBTREE)
    #     print(res) # search是否成功（True，False）
    #     print(conn.result) # 查询失败的原因
    #     print(conn.entries) #查询到的数据
    #     if res:
    #         entry = conn.response[0]
    #         dn = entry['dn']
    #         attr_dict =entry['attributes']
    #         print(attr_dict["mail"])
    #         print(attr_dict["cn"])
    #         print(isinstance(attr_dict,dict))
    #         try:
    #             # res_try = conn.extend.microsoft.modify_password('CN=YouhaiWang,OU=Data-Platform,OU=RD,OU=BeiJing,OU=aibee,DC=aibee,DC=cn','Wangyouhai@753')#修改密码
    #             conn2 = Connection(host,user=dn,password=password,check_names=True,lazy=False,raise_exceptions=False)
    #             conn2.bind()
    #             if conn2.result['description'] == 'success':
    #                 print("auth true")
    #                 return True
    #             else:
    #                 print("auth fail")
    #                 return False
    #         except Exception as e:
    #             print("auth fail")
    #             return False
    # except Exception as e:
    #     print("auth fail")
    #     return False
