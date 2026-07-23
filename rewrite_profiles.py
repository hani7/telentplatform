import re

def process_template(filepath, context_var):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Make sure we load player_tags
    if '{% load player_tags %}' not in content:
        content = content.replace('{% load static %}', '{% load static %}\n{% load player_tags %}')

    # 1. Update CSS
    # Let's replace the whole <style> block if it exists, or just use regex to replace specific rules.
    # It's easier to just replace the body and specific components.
    
    css_updates = [
        # Body
        (r'body\s*\{[^}]*background:[^}]*\}', 'body { background: #f4f6f9; color: #1a1a1a; font-family: \'Inter\', sans-serif; padding-bottom: 90px; }'),
        # p-header
        (r'\.p-header\s*\{[^}]*\}', '.p-header { background: #ffffff; padding: 2.5rem 1.5rem 1.5rem; text-align: center; position: relative; border-bottom: 1px solid #e9ecef; box-shadow: 0 2px 10px rgba(0,0,0,0.02); }'),
        # p-name
        (r'\.p-name\s*\{[^}]*\}', '.p-name { font-size: 1.6rem; font-weight: 800; margin: 0 0 0.5rem; color: #1a1a1a; display: flex; align-items: center; justify-content: center; gap: 8px; }'),
        # p-tag
        (r'\.p-tag\s*\{[^}]*\}', '.p-tag { background: #f8f9fa; border: 1px solid #e9ecef; padding: 5px 12px; border-radius: 50px; font-size: 0.8rem; font-weight: 600; display: flex; align-items: center; gap: 6px; color: #495057; }'),
        # p-tag-gold
        (r'\.p-tag-gold\s*\{[^}]*\}', '.p-tag-gold { background: rgba(241, 177, 15, 0.1); border-color: rgba(241, 177, 15, 0.2); color: #d49a0d; }'),
        # p-tag-green
        (r'\.p-tag-green\s*\{[^}]*\}', '.p-tag-green { background: rgba(29, 185, 91, 0.1); border-color: rgba(29, 185, 91, 0.2); color: #1a9e4d; }'),
        # badge-mineur
        (r'\.badge-mineur\s*\{[^}]*\}', '.badge-mineur { position: absolute; bottom: -5px; left: 50%; transform: translateX(-50%); background: #e74c3c; color: #fff; font-size: 0.65rem; font-weight: 800; padding: 3px 8px; border-radius: 50px; border: 2px solid #ffffff; text-transform: uppercase; letter-spacing: 0.05em; }'),
        # avatar
        (r'\.p-avatar\s*\{[^}]*\}', '.p-avatar { width: 100%; height: 100%; border-radius: 50%; object-fit: cover; border: 3px solid #f1b10f; box-shadow: 0 4px 15px rgba(241, 177, 15, 0.15); background: #f8f9fa; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; color: #ced4da; }'),
        # cards (.ic)
        (r'\.ic\s*\{[^}]*\}', '.ic { background: #ffffff; border: 1px solid #e9ecef; border-radius: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.02); padding: 1.2rem; margin-bottom: 1rem; }'),
        (r'\.ic h5\s*\{[^}]*\}', '.ic h5 { margin-top: 0; font-size: 1.1rem; color: #1a1a1a; margin-bottom: 1rem; display: flex; align-items: center; gap: 8px; font-weight: 800; border-bottom: 1px solid #f1f3f5; padding-bottom: 10px; }'),
        (r'\.il\s*\{[^}]*\}', '.il { color: #6c757d; font-size: 0.85rem; font-weight: 500; flex: 1; }'),
        (r'\.iv\s*\{[^}]*\}', '.iv { color: #212529; font-weight: 700; font-size: 0.9rem; text-align: right; max-width: 60%; }'),
        (r'\.iv\.empty\s*\{[^}]*\}', '.iv.empty { color: #adb5bd; font-weight: 400; font-style: italic; }'),
        # tabs
        (r'\.ptabs\s*\{[^}]*\}', '.ptabs { display: flex; gap: 4px; padding: 10px 14px; background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); border-bottom: 1px solid #e9ecef; box-shadow: 0 4px 15px rgba(0,0,0,0.03); margin-bottom: 1rem; position: sticky; top: 0; z-index: 1000; overflow-x: auto; white-space: nowrap; -webkit-overflow-scrolling: touch; }'),
        (r'\.ptab\s*\{[^}]*\}', '.ptab { flex: 1; min-width: max-content; background: none; border: none; padding: 8px 12px; color: #6c757d; font-weight: 600; font-size: 0.9rem; cursor: pointer; transition: all 0.2s; border-radius: 8px; display: flex; align-items: center; justify-content: center; gap: 6px; }'),
        (r'\.ptab\.active\s*\{[^}]*\}', '.ptab.active { background: #e8f8f0; color: #1db95b; }'),
    ]

    for pattern, replacement in css_updates:
        content = re.sub(pattern, replacement, content)
        
    # Hide header-area if not already hidden
    if '.header-area' not in content[:3000]:
        # add to style block
        content = content.replace('</style>', '  /* Hide Global Header for Profile */\n  .header-area { display: none !important; }\n  .back-btn-fixed { background: #ffffff !important; color: #1a1a1a !important; border: 1px solid #e9ecef !important; box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important; }\n</style>')

    # 2. Add Flag URL logic
    # Find nationality tag and replace it
    # <i class="ti ti-flag"></i> {{ profile.nationality|default:"International" }}
    flag_pattern = r'<i class="ti ti-flag"></i>\s*\{\{\s*' + context_var + r'\.nationality\|default:"International"\s*\}\}'
    flag_replacement = f'''{{% if {context_var}.nationality %}}
          {{% with f_url={context_var}.nationality.name|flag_url %}}
            {{% if f_url %}}
              <img src="{{{{ f_url }}}}" alt="{{{{ {context_var}.nationality.name }}}}" class="flag-img" style="width: 20px; border-radius: 2px;">
            {{% else %}}
              <i class="ti ti-flag"></i>
            {{% endif %}}
          {{% endwith %}}
          {{{{ {context_var}.nationality.name }}}}
        {{% else %}}
          <i class="ti ti-flag"></i> International
        {{% endif %}}'''
    
    content = re.sub(flag_pattern, flag_replacement, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# We need to process profile_complete.html
process_template('templates/players/profile_complete.html', 'profile')

# We need to rebuild public_profile.html to use tabs as well!
# Actually, the user asked to "use fixed menu ancre in the top of all sections".
# So public_profile.html needs to have the EXACT same HTML structure as profile_complete.html, but with p instead of profile.
with open('templates/players/profile_complete.html', 'r', encoding='utf-8') as f:
    complete_html = f.read()

# We need to adapt it for public_profile (extends base.html, uses `p` instead of `profile`)
public_html = complete_html.replace('{{ profile.', '{{ p.').replace('{% if profile.', '{% if p.').replace('profile.pk', 'p.pk').replace('profile.profile_status', 'p.profile_status')

# But public_profile.html should extend base.html
# Let's extract everything inside <body>...</body> and put it in {% block content %}
body_match = re.search(r'<body[^>]*>(.*)</body>', public_html, re.DOTALL)
if body_match:
    body_content = body_match.group(1)
    
    # Extract style block
    style_match = re.search(r'<style>(.*?)</style>', public_html, re.DOTALL)
    style_content = style_match.group(1) if style_match else ""
    
    final_public = f'''{{% extends "base.html" %}}
{{% load static %}}
{{% load player_tags %}}
{{% block title %}}{{{{ p.first_name }}}} {{{{ p.last_name }}}} - Profil{{% endblock %}}

{{% block extra_css %}}
<style>
{style_content}
</style>
{{% endblock %}}

{{% block content %}}
{body_content}
{{% endblock %}}
'''
    with open('templates/players/public_profile.html', 'w', encoding='utf-8') as f:
        f.write(final_public)

