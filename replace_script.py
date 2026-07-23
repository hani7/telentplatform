import os

replacements = {
    '⚽': '<i class="ti ti-ball-football"></i>',
    '⏳': '<i class="ti ti-hourglass"></i>',
    '✅': '<i class="ti ti-check"></i>',
    '❌': '<i class="ti ti-x"></i>',
    '🎂': '<i class="ti ti-calendar"></i>',
    '📊': '<i class="ti ti-chart-bar"></i>',
    '👁️': '<i class="ti ti-eye"></i>',
    '🎥': '<i class="ti ti-movie"></i>',
    '🖼️': '<i class="ti ti-photo"></i>',
    '📄': '<i class="ti ti-file-text"></i>',
    '📎': '<i class="ti ti-paperclip"></i>',
    '📁': '<i class="ti ti-folder"></i>'
}

files_to_check = [
    'templates/offline.html',
    'templates/offers/my_offers.html',
    'templates/offers/my_suggestions.html',
    'templates/players/public_profile.html'
]

for file in files_to_check:
    path = os.path.join(*file.split('/'))
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        for emoji, icon in replacements.items():
            content = content.replace(emoji, icon)
            
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
print('Emojis replaced!')
