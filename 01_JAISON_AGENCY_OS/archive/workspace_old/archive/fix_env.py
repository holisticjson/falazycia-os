content = open("/home/holisticjson/hermes-agent/.env").read()
content = content.replace("sk-hermes-local", "dummy-key")
open("/home/holisticjson/hermes-agent/.env", "w").write(content)
