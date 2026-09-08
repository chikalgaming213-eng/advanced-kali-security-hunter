from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

W, H = 1600, 980
img = Image.new('RGB', (W, H), '#091017')
d = ImageDraw.Draw(img)
try:
    regular = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 20)
    small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 15)
    bold = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24)
    title = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30)
except OSError:
    regular = small = bold = title = ImageFont.load_default()

sidebar = 300
d.rectangle((0, 0, sidebar, H), fill='#0d1922')
d.rectangle((sidebar, 0, W, 82), fill='#101d27')
d.text((28, 28), 'BUG BOUNTY HUNTER X', fill='#52e0bd', font=bold)
items = ['MAIN SECURITY HUNTER','DEFENSE MONSTER SOC','ANTI DOS / DDOS MONITOR','MALWARE RISK MONITOR','UBUNTU KDE ENVIRONMENT','DEBIAN XFCE ENVIRONMENT','ADVANCED TERMINAL','METASPLOIT WORKSPACE','TOOL CENTER','RECON CENTER','WEB / API SECURITY','NETWORK CENTER','OSINT CENTER','EVIDENCE CENTER','REPORT CENTER','SYSTEM MONITOR','SETTINGS','AUDIT LOGS']
for i, item in enumerate(items):
    y = 105 + i * 42
    if i == 0: d.rounded_rectangle((14, y-8, sidebar-14, y+28), radius=6, fill='#00a878')
    d.text((28, y), item, fill='white' if i == 0 else '#b7c8d1', font=small)

d.text((335, 28), 'UNIFIED SECURITY WORKSTATION', fill='#e2edf2', font=title)
d.text((335, 96), 'MAIN SECURITY HUNTER  |  READ_ONLY', fill='#52e0bd', font=bold)

cards = [('CPU', 36, '#00a878'), ('RAM', 52, '#2b9ed8'), ('DISK', 41, '#c59d3d'), ('THREAT SCORE', 18, '#4b9b73')]
for i, (label, value, color) in enumerate(cards):
    x = 335 + i * 290
    d.rounded_rectangle((x, 145, x+260, 245), radius=8, fill='#111d26', outline='#294451', width=2)
    d.text((x+18, 162), label, fill='#a9bdc7', font=small)
    d.text((x+18, 192), f'{value}%', fill=color, font=bold)
    d.rectangle((x+105, 198, x+235, 214), fill='#20323d')
    d.rectangle((x+105, 198, x+105+int(130*value/100), 214), fill=color)

d.rounded_rectangle((335, 275, 920, 470), radius=8, fill='#111d26', outline='#294451', width=2)
d.text((360, 298), 'AUTHORIZED TARGET SCOPE', fill='#52e0bd', font=bold)
d.rounded_rectangle((360, 345, 890, 395), radius=5, fill='#182a35')
d.text((380, 359), '127.0.0.1', fill='#d7e3ea', font=regular)
d.rounded_rectangle((360, 415, 610, 455), radius=5, fill='#00a878')
d.text((390, 425), 'START READ-ONLY ASSESSMENT', fill='white', font=small)

d.rounded_rectangle((950, 275, 1565, 470), radius=8, fill='#111d26', outline='#294451', width=2)
d.text((975, 298), 'DEFENSE MONSTER SOC', fill='#52e0bd', font=bold)
for j, text in enumerate(['Firewall: DETECTED / READ-ONLY','IDS: LOCAL ANALYSIS ONLY','DoS/DDoS: 0 active indicators','Malware risk: review signals only','Response mode: MANUAL']):
    d.text((980, 345 + j*28), '●  ' + text, fill='#c9d7dc', font=small)

d.rounded_rectangle((335, 500, 1565, 885), radius=8, fill='#111d26', outline='#294451', width=2)
d.text((360, 525), 'LIVE SECURITY EVENTS / REPORT OUTPUT', fill='#52e0bd', font=bold)
logs = ['100%  Assessment completed', ' 89%  finding_correlation', ' 78%  endpoint_discovery', ' SOC   no automatic response executed', ' GUI   JSON / HTML / Markdown / TXT reports ready']
for j, text in enumerate(logs): d.text((370, 585+j*42), text, fill='#c9d7dc', font=regular)
d.text((335, 930), 'Local • Database-free • Authorized scope • No retaliation • No automatic destructive response', fill='#6f8792', font=small)

out = Path(__file__).parent / 'images' / 'unified_gui.png'
out.parent.mkdir(parents=True, exist_ok=True)
img.save(out)
print(out)
