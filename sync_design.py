import re

with open('templates/players/public_profile.html', encoding='utf-8') as f:
    content = f.read()

# Replace p with profile
content = content.replace('{{ p.', '{{ profile.')
content = content.replace('{% if p.', '{% if profile.')
content = content.replace('{% elif p.', '{% elif profile.')
content = content.replace('p.pk', 'profile.pk')
content = content.replace('request.user == p.user', 'request.user == profile.user')
content = content.replace('in p.', 'in profile.')

# Update footer active states
content = content.replace('href="{% url \'players:public_profile\' profile.pk %}" class="footer-pill-item is-active"', 'href="{% url \'players:public_profile\' profile.pk %}" class="footer-pill-item"')
content = content.replace('href="{% url \'players:public_profile\' p.pk %}" class="footer-pill-item is-active"', 'href="{% url \'players:public_profile\' profile.pk %}" class="footer-pill-item"')
content = content.replace('href="{% url \'players:profile_complete\' %}" class="footer-pill-item"', 'href="{% url \'players:profile_complete\' %}" class="footer-pill-item is-active"')

with open('templates/players/profile_complete.html', 'w', encoding='utf-8') as f:
    f.write(content)
