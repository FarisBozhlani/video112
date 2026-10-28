from pathlib import Path
import math,wave,struct
p=Path('/workspace/video-edit')
segments=[(0,3,'alejhi selam. Allahu alejhi ve sellem në një hadith atë'),(3,7,'ka shpëtuar ai njeri që i ka këto tri'),(7,10,'cilësi, këto tri veti.'),(10,14,'Ka shpëtuar ai njeri i cili është udhëzuar në Islam,'),(14,19,'sepse vetëm Islam i garanton shpëtimin në këtë botë dhe në botën tjetër.'),(19,22,'Dhe thotë pejgamberi alejhi selam,'),(22,27,'ka shpëtuar ai njeri që është furnizuar me atë që i mjafton.'),(27,34,'Pra ka shpëtuar ai që i ka gjërat që i mjaftojnë për jetën e tij të përditshme.'),(34,39,'Sepse ai që i ka gjërat që i mjaftojnë, nuk ka nevojë'),(39,42,"që t’ia zgjat dorën njerëzve."),(42,44,'Ai që i ka gjërat që i mjaftojnë,'),(44,48,"nuk ka nevojë që t’i shkojë syri te pasuria e tjetrit,"),(48,54,'dhe nuk ka nevojë që ta nënshtrojë veten edhe ta përul veten para njerëzve.'),(54,58,'Dhe e treta është, thotë pejgamberi alejhi selam,'),(58,64,'ka shpëtuar ai njeri që Allahu e ka bërë të kënaqur me atë që e ka jap.'),(64,76.55,'Ka shpëtuar ai i cili ka arritur që me caktimin e Allahut të jetë i kënaqur me ato gjëra që ia ka nda Allahu edhe ia ka caktuar Allahu subhanehu ue teala.')]
def ts(t):
 c=round(t*100);return f'{c//360000}:{c//6000%60:02}:{c//100%60:02}.{c%100:02}'
head='''[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,DejaVu Sans,66,&H00FFFFFF,&H0000E5FF,&H00101810,&H80000000,-1,0,0,0,100,100,0,0,1,5,2,5,75,75,0,1
Style: Title,DejaVu Sans,77,&H00FFFFFF,&H0000E5FF,&H00101810,&H80000000,-1,0,0,0,100,100,0,0,1,3,1,5,55,55,0,1
Style: Card,DejaVu Sans,37,&H00FFFFFF,&H0000E5FF,&H00101810,&H80000000,-1,0,0,0,100,100,0,0,1,2,0,5,50,50,0,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
events=[]
def ev(a,b,style,txt,layer=2):events.append(f'Dialogue: {layer},{ts(a)},{ts(b)},{style},,0,0,0,,{txt}')
ev(0,3,'Title',r'{\pos(540,270)\fad(80,180)\fscx85\fscy85\t(0,160,\fscx105\fscy105)\t(160,280,\fscx100\fscy100)\1c&H00E5FF&}3 CILËSI\N{\fs53\1c&HFFFFFF&}TË NJERIUT QË\NKA SHPËTUAR')
# Short, phrase-level captions, timed within the supplied transcript anchors.
for a,b,txt in segments:
 words=txt.split(); chunks=[words[i:i+4] for i in range(0,len(words),4)]; total=sum(len(' '.join(x)) for x in chunks); t=a
 for ch in chunks:
  d=(b-a)*len(' '.join(ch))/total
  line=' '.join(ch).upper()
  ev(t,t+d,'Caption',r'{\pos(540,1210)\fad(45,45)\fscx94\fscy94\t(0,110,\fscx105\fscy105)\t(110,190,\fscx100\fscy100)\1c&H00E5FF&}'+line)
  t+=d
for a,b,n,label in [(10,19,'01','UDHËZIMI NË ISLAM'),(22,54,'02','AJO QË TË MJAFTON'),(58,73,'03','KËNAQËSIA')]:
 ev(a,b,'Card',r'{\an5\pos(540,1660)\fad(160,180)\p1\bord0\shad0\1c&H201810&\alpha&H18&}m -465 -65 l 465 -65 l 465 65 l -465 65',0)
 ev(a,b,'Card',r'{\move(540,1700,540,1660,0,220)\fad(120,150)\1c&H8AC815&}'+n+r'  {\1c&HFFFFFF&}'+label)
ev(73,76.55,'Card',r'{\pos(540,1660)\fad(180,180)\1c&H8AC815&}ISLAMI  •  MJAFTUESHMËRIA\N KËNAQËSIA')
(p/'captions.ass').write_text(head+'\n'.join(events),encoding='utf-8')
# Restrained original transition accents; no external music assets.
rate=48000; dur=76.65; cues=[0,10,22,58]; audio=[0.0]*int(rate*dur)
for start in cues:
 for i in range(int(.24*rate)):
  t=i/rate; amp=.045*math.exp(-t*22); v=amp*(math.sin(2*math.pi*(180*t-220*t*t))+.25*math.sin(2*math.pi*900*t)); j=int(start*rate)+i
  if j<len(audio): audio[j]+=v
with wave.open(str(p/'cues.wav'),'w') as w:
 w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate);w.writeframes(b''.join(struct.pack('<h',max(-32767,min(32767,int(x*32767)))) for x in audio))
# Periodic digital crop changes; retain the original continuous speech.
filtergraph="[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z='if(lt(on,12),1.13-on*0.006,if(eq(mod(floor(on/96),2),0),1.015,1.095))':x='iw/2-iw/zoom/2':y='ih*0.28-ih*0.28/zoom':d=1:s=1080x1920:fps=30,eq=contrast=1.045:saturation=0.96:brightness=-0.012,drawbox=x=0:y=1510:w=iw:h=410:color=0x101820@0.70:t=fill,ass=/workspace/video-edit/captions.ass[v];[0:a]highpass=f=75,acompressor=threshold=0.18:ratio=2:attack=10:release=150[a];[a][1:a]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[outa]"
(p/'filter.txt').write_text(filtergraph)
