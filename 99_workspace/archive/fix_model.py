with open('/home/holisticjson/.hermes/config.yaml', 'r') as f:
    c = f.read()
c = c.replace('default: groq/llama3-70b-8192', 'default: smart-logic')
with open('/home/holisticjson/.hermes/config.yaml', 'w') as f:
    f.write(c)
print("Config updated.")
