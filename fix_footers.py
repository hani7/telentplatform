import os
import re

css_to_find = r'\.footer-pill\s*\{.*?\}.*?\.footer-pill-item\s*\{.*?\}'
css_replacement = '''
.footer-pill {
  background: #1db95b;
  border-radius: 999px;
  display: flex;
  align-items: center;
  justify-content: space-around;
  padding: 6px 8px;
  width: 100%;
  max-width: 480px;
  box-shadow: 0 10px 25px rgba(29,185,91,0.3);
}
.footer-pill-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  color: rgba(255,255,255,0.85);
  text-decoration: none;
  font-size: 0.65rem;
  font-weight: 500;
  padding: 6px 2px;
  border-radius: 14px;
  transition: all 0.2s ease;
  flex: 1;
  min-width: 0;
  text-align: center;
}
'''.strip()

def fix_footer_css(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We will just replace any occurrence of the old minified or unminified CSS blocks for .footer-pill and .footer-pill-item
    # Since regex can be tricky with multiline, let's just find and replace the specific lines if they exist, or use a regex with re.DOTALL
    
    # First, let's just use re.sub with DOTALL to replace from .footer-pill { to the end of .footer-pill-item.is-active i { ... }
    # Actually, it's safer to just replace the two main classes
    
    # Find .footer-pill { ... }
    new_content = re.sub(r'\.footer-pill\s*\{[^}]*\}', '.footer-pill { background: #1db95b; border-radius: 999px; display: flex; align-items: center; justify-content: space-around; padding: 6px 8px; width: 100%; max-width: 480px; box-shadow: 0 10px 25px rgba(29,185,91,0.3); }', content)
    
    # Find .footer-pill-item { ... }
    new_content = re.sub(r'\.footer-pill-item\s*\{[^}]*\}', '.footer-pill-item { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px; color: rgba(255,255,255,0.85); text-decoration: none; font-size: 0.65rem; font-weight: 500; padding: 6px 2px; border-radius: 14px; transition: all 0.2s ease; flex: 1; min-width: 0; text-align: center; overflow: hidden; }', new_content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed {filepath}")

for root, dirs, files in os.walk('templates'):
    for file in files:
        if file.endswith('.html'):
            fix_footer_css(os.path.join(root, file))
