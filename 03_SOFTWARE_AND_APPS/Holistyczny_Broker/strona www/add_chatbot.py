import glob
import re

script_tag = '\n    <script src="chatbot-ui.js"></script>\n</body>'

for filepath in glob.glob("*.html"):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'chatbot-ui.js' not in content:
        # replace </body> with script + </body>
        content = re.sub(r'</body>', script_tag, content, flags=re.IGNORECASE)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Added chatbot to {filepath}")
