with open('/home/holisticjson/.hermes/config.yaml', 'r') as f:
    c = f.read()
c = c.replace('default: smart-logic', 'default: secure-vault')
with open('/home/holisticjson/.hermes/config.yaml', 'w') as f:
    f.write(c)
print("Config updated to secure-vault.")
