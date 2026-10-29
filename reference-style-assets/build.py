from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import random,json
p=Path('/workspace/reference-edit');r=random.Random(12)
bold='/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf'
def font(n):return ImageFont.truetype(bold,n)
def paper(w,h):
 im=Image.new('RGB',(w,h),(236,232,217));d=ImageDraw.Draw(im)
 for i in range(w*h//8):
  x=r.randrange(w);y=r.randrange(h);v=r.randrange(211,245);d.point((x,y),fill=(v,v-2,v-9))
 return im
bg=paper(1080,1920);d=ImageDraw.Draw(bg)
for x in range(0,1080,48):d.line((x,0,x,1920),fill=(211,211,196))
for y in range(0,1920,48):d.line((0,y,1080,y),fill=(211,211,196))
d.polygon([(0,0),(1080,0),(1080,75),(0,115)],fill='#177d79')
d.rectangle((50,125,1030,305),fill='#f1cf32')
d.rectangle((58,338,1038,1620),fill='#a7a291');d.rectangle((40,322,1020,1604),fill='#faf7ee')
d.polygon([(20,305),(260,282),(275,347),(30,372)],fill='#dfc331');d.polygon([(840,1580),(1060,1550),(1070,1610),(850,1640)],fill='#258c84')
d.text((70,1730),'TRI CILËSI.',font=font(62),fill='#202625');d.text((70,1810),'NJË MESAZH PËR JETËN.',font=font(31),fill='#237a74')
d.line([(870,1700),(920,1660),(920,1740)],fill='#ba4334',width=8)
bg.save(p/'background.png')
for n,title,subtitle in [(1,'UDHËZIMI','NË ISLAM'),(2,'MJAFTUESHMËRIA','AJO QË TË MJAFTON'),(3,'KËNAQËSIA','ME CAKTIMIN E ALLAHUT')]:
 im=paper(920,620).convert('RGBA');d=ImageDraw.Draw(im)
 # Rough torn lower edge, tape and editorial rules.
 for x in range(0,920,12):d.polygon([(x,600+r.randrange(18)),(x+12,600+r.randrange(18)),(x+12,620),(x,620)],fill=(0,0,0,0))
 d.polygon([(30,24),(250,8),(260,63),(35,80)],fill='#e8cb32');d.text((48,25),f'0{n}',font=font(51),fill='#1c615c')
 d.text((45,105),title,font=font(63 if n!=2 else 53),fill='#191e1e');d.text((48,186),subtitle,font=font(30),fill='#266f69')
 d.line((45,246,875,246),fill='#292c2b',width=3)
 if n==1:
  d.polygon([(370,540),(445,295),(495,295),(570,540)],fill='#227d76')
  for y in [340,400,460]:d.rectangle((462,y,476,y+26),fill='#f1ce36')
  d.ellipse((620,300,745,425),fill='#e8cc38');d.line((335,548,610,548),fill='#202524',width=7)
 elif n==2:
  d.rectangle((100,370,300,520),fill='#237d76');d.polygon([(75,375),(200,280),(325,375)],fill='#202524');d.rectangle((180,440,230,520),fill='#e8cc38')
  d.pieslice((395,320,635,550),0,180,fill='#227d76');d.line((395,430,635,430),fill='#202524',width=7)
  d.rounded_rectangle((720,310,805,530),radius=18,fill='#e8cc38',outline='#202524',width=5)
 else:
  d.ellipse((310,290,490,470),fill='#247e77');d.ellipse((455,290,635,470),fill='#247e77');d.polygon([(323,423),(622,423),(472,565)],fill='#247e77');d.line([(430,430),(467,468),(535,380)],fill='#f2d13c',width=12)
 im.save(p/f'card{n}.png')
# Reuse the verified word events, with compact captions matching the reference.
s=Path('/workspace/video-overhaul/captions.ass').read_text();header=s.split('[Events]')[0].replace('Style: Cap,DejaVu Sans,75','Style: Cap,DejaVu Sans,57')
lines=[]
for line in s.splitlines():
 if line.startswith('Dialogue: 6,'):
  lines.append(line.replace(r'\pos(540,1110)',r'\pos(540,1300)'))
def ts(t):
 c=round(t*100);return f'{c//360000}:{c//6000%60:02}:{c//100%60:02}.{c%100:02}'
for a,b,t in [(0,3,'3 CILËSI PËR JETËN'),(3,16,'01  UDHËZIMI NË ISLAM'),(16,29,'02  AJO QË TË MJAFTON'),(29,45.7,'03  TË JESH I KËNAQUR')]:
 lines.append(f'Dialogue: 4,{ts(a)},{ts(b)},Head,,0,0,0,,{{\\pos(540,210)\\fs54\\1c&H202020&\\bord0\\fad(100,100)}}{t}')
(p/'captions.ass').write_text(header+'[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'+'\n'.join(lines))
# Keep the existing editorial cut and mastered sound, replace the entire visual composition.
s=Path('/workspace/video-overhaul/filter.txt').read_text();a=s.index('[cut]scale=');b=s.index(';[voice]',a)
v="[cut]scale=940:1250:force_original_aspect_ratio=increase,crop=940:1250,zoompan=z='if(eq(mod(floor(on/75),2),0),1.02,1.13)':x='iw/2-iw/zoom/2':y='ih*0.23-ih*0.23/zoom':d=1:s=940x1250:fps=30,eq=contrast=1.05:saturation=0.88[panel];[2:v][panel]overlay=x='70+8*sin(t*1.4)':y='350+5*sin(t)' :shortest=1[base];[base][3:v]overlay=80:870:enable='between(t,7.5,10)+between(t,12.5,15)'[c1];[c1][4:v]overlay=80:870:enable='between(t,17,19.5)+between(t,24,26.5)'[c2];[c2][5:v]overlay=80:870:enable='between(t,36,38.5)+between(t,41,43.5)'[c3];[c3]ass=/workspace/reference-edit/captions.ass[v]"
(p/'filter.txt').write_text(s[:a]+v+s[b:])
