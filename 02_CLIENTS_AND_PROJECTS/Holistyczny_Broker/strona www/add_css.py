import glob
import re

css_tag = '\n    <link rel="stylesheet" href="chatbot-ui.css">\n</head>'

for filepath in glob.glob("*.html"):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'chatbot-ui.css' not in content:
        content = re.sub(r'</head>', css_tag, content, flags=re.IGNORECASE)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Added CSS to {filepath}")
