import subprocess

wrapper_html = '''<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    html, body { width: 360px; height: 800px; overflow: hidden; background: #020617; }
    iframe { width: 360px; height: 800px; border: none; }
  </style>
</head>
<body>
  <iframe src="index.html"></iframe>
</body>
</html>
'''

with open('wrapper_shot.html', 'w', encoding='utf-8') as f:
    f.write(wrapper_html)

# Mobile 360x800 screenshot
subprocess.run([
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--disable-gpu',
    '--window-size=360,800',
    r'--screenshot=C:\Users\umutc\.gemini\antigravity\scratch\kelime-avcisi\screen_mobile_masterpiece.png',
    r'file:///C:/Users/umutc/.gemini/antigravity/scratch/kelime-avcisi/wrapper_shot.html'
])

# Desktop 1280x800 screenshot
subprocess.run([
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--disable-gpu',
    '--window-size=1280,800',
    r'--screenshot=C:\Users\umutc\.gemini\antigravity\scratch\kelime-avcisi\screen_desktop_masterpiece.png',
    r'file:///C:/Users/umutc/.gemini/antigravity/scratch/kelime-avcisi/index.html'
])

print("Both screenshots captured successfully!")
