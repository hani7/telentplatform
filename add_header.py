import re

with open('templates/players/profile_complete.html', encoding='utf-8') as f:
    content = f.read()

header_html = """
    <!-- Profile Header -->
    <div class="p-header" style="margin-bottom:1.5rem; text-align:center;">
      <div class="p-avatar-wrap">
        {% if profile.profile_photo %}
          <img src="{{ profile.profile_photo.url }}" alt="Photo de profil" class="p-avatar">
        {% else %}
          <div class="p-avatar"><i class="ti ti-user"></i></div>
        {% endif %}
        {% if profile.is_minor %}
          <div class="badge-mineur">MINEUR</div>
        {% endif %}
      </div>

      <h1 class="p-name">
        {{ profile.first_name }} {{ profile.last_name }}
        {% if profile.is_active %}<i class="ti ti-discount-check-filled p-verified" title="Vérifié"></i>{% endif %}
      </h1>

      <div class="p-tags">
        <!-- Account Status -->
        {% if profile.profile_status == 'ACTIVE' %}
          <div class="p-tag" style="background:rgba(16, 185, 129, 0.15); color:#10b981; border-color:rgba(16, 185, 129, 0.3);">
            <i class="ti ti-circle-check"></i> Compte Actif
          </div>
        {% else %}
          <div class="p-tag" style="background:rgba(245, 158, 11, 0.15); color:#f59e0b; border-color:rgba(245, 158, 11, 0.3);">
            <i class="ti ti-clock"></i> En attente de validation
          </div>
        {% endif %}
        <!-- Club Logo & Name -->
        <div class="p-tag p-tag-green">
          <i class="ti ti-shield"></i> {{ profile.current_club_name|default:"Libre" }}
        </div>
        <!-- Nationality -->
        <div class="p-tag">
          <i class="ti ti-flag"></i> {{ profile.nationality|default:"International" }}
        </div>
        <!-- Age -->
        {% if profile.age %}
        <div class="p-tag">
          <i class="ti ti-calendar"></i> {{ profile.age }} ans
        </div>
        {% endif %}
        <!-- Position -->
        <div class="p-tag p-tag-gold">
          <i class="ti ti-shoe"></i> {{ profile.position|default:"Non spécifié" }}
        </div>
        <!-- Foot -->
        {% if profile.get_foot_display %}
        <div class="p-tag">
          <i class="ti ti-footprints"></i> Pied: {{ profile.get_foot_display }}
        </div>
        {% endif %}
      </div>
    </div>
"""

content = content.replace('<div class="content">', '<div class="content">\n' + header_html)

# Also fix the footer to have 5 items instead of 6 by removing the 'Actif' footer item, since we moved it to the header!
footer_start = content.find('{% if profile.profile_status == \'ACTIVE\' %}')
footer_end = content.find('{% endif %}', footer_start) + len('{% endif %}')
if footer_start != -1:
    content = content[:footer_start] + content[footer_end:]

with open('templates/players/profile_complete.html', 'w', encoding='utf-8') as f:
    f.write(content)
