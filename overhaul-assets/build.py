from pathlib import Path
import json,math,wave,struct,random
p=Path('/workspace/video-overhaul')
segments=json.loads((p/'transcript.json').read_text())
clips=[(3,19),(22,27),(34,42),(54,58),(64,76.65)]; duration=sum(b-a for a,b in clips)
def ts(t):
 c=round(t*100);return f'{c//360000}:{c//6000%60:02}:{c//100%60:02}.{c%100:02}'
head='''[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,DejaVu Sans,75,&H00FFFFFF,&H0000E5FF,&H00101810,&H70000000,-1,0,0,0,100,100,-1,0,1,5,2,5,70,70,0,1
Style: Head,DejaVu Sans,68,&H00FFFFFF,&H0000E5FF,&H00101810,&H70000000,-1,0,0,0,100,100,-1,0,1,1,0,5,55,55,0,1
Style: Small,DejaVu Sans,30,&H00FFFFFF,&H0000E5FF,&H00101810,&H70000000,-1,0,0,0,100,100,2,0,1,0,0,5,30,30,0,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
e=[]
def ev(a,b,style,text,layer=2):e.append(f'Dialogue: {layer},{ts(a)},{ts(b)},{style},,0,0,0,,{text}')
def rect(a,b,x,y,w,h,color,layer=0):ev(a,b,'Small',f'{{\\an7\\pos({x},{y})\\p1\\bord0\\shad0\\1c&H{color}&}}m 0 0 l {w} 0 l {w} {h} l 0 {h}',layer)
rect(0,duration,0,0,1080,270,'201810');rect(0,duration,0,1430,1080,490,'201810')
ev(0,3,'Head',r'{\pos(540,125)\fad(50,120)\fscx75\fscy75\t(0,140,\fscx107\fscy107)\t(140,230,\fscx100\fscy100)}3 CILËSI.\N{\1c&H00E5FF&}NJË SHPËTIM.')
ev(3,duration,'Small',r'{\pos(540,75)\1c&H8AC815&}TRI CILËSI • NJË MESAZH')
# Section navigation, advancing rather than restarting at each cut.
for a,b,num,title,sub in [(3,16,'01','ISLAMI','UDHËZIMI'),(16,29,'02','MJAFTUESHMËRIA','AJO QË TË MJAFTON'),(29,duration,'03','KËNAQËSIA','ME CAKTIMIN E ALLAHUT')]:
 ev(a,b,'Head',r'{\pos(540,170)\fad(120,100)\1c&H00E5FF&}'+num+r'  {\1c&HFFFFFF&\fs56}'+title)
 ev(a,b,'Small',r'{\pos(540,1750)\fad(140,100)\1c&H8AC815&}'+sub)
 # Large numeral and bespoke minimalist vector icon next to it.
 ev(a,min(a+1.2,b),'Head',r'{\move(930,500,930,430,0,240)\fad(80,220)\fs140\1c&H00E5FF&}'+num)
# Word-level kinetic captions anchored to the supplied transcript timestamps.
word_times=[]
off=0
for ca,cb in clips:
 for a,b,text in segments:
  if a<ca or b>cb+0.01:continue
  words=text.split(); weights=[max(2,len(w)) for w in words]; total=sum(weights);t=off+a-ca
  for k,word in enumerate(words):
   d=(b-a)*weights[k]/total
   group_start=(k//3)*3; group=words[group_start:group_start+3]; parts=[]
   for j,w in enumerate(group):
    active=(group_start+j==k)
    tag=r'{\1c&H00E5FF&\fscx116\fscy116\t(0,95,\fscx100\fscy100)}' if active else r'{\1c&HFFFFFF&\fscx100\fscy100}'
    parts.append(tag+w.upper())
   ev(t,t+d,'Cap',r'{\pos(540,1110)\fad(15,15)}'+' '.join(parts),6)
   word_times.append(t);t+=d
 off+=cb-ca
# Closing line stays in its own footer while the voice concludes.
ev(duration-3,duration,'Small',r'{\pos(540,1830)\fad(100,100)}ISLAMI  /  MJAFTUESHMËRIA  /  KËNAQËSIA')
# Advancing segmented progress track.
for i in range(90):
 a=i*duration/90;rect(a,duration,90+i*10,1870,8,6,'8AC815')
# Explanatory vector illustrations: path, bowl, heart; all avoid the face.
icons=[(3,16,'m 0 85 l 40 5 l 80 85 m 40 5 l 40 90 m 15 55 l 65 55'),(16,29,'m 0 30 b 0 100 100 100 100 30 l 0 30 m 10 10 l 90 10'),(29,duration,'m 50 95 b -35 40 0 -15 50 20 b 100 -15 135 40 50 95')]
for a,b,path in icons:ev(a,b,'Small',r'{\pos(130,1730)\an5\p1\fscx80\fscy80\bord2\shad0\1c&H8AC815&\3c&H8AC815&\fad(180,180)}'+path)
# Original full-screen conceptual cutaways; narration and captions remain continuous.
cutaways=[(7.5,10,'01','UDHËZIMI NË ISLAM','NJË RRUGË E QARTË','m 0 250 l 120 0 l 240 250 m 120 0 l 120 250'),(17,19.5,'02','AJO QË TË MJAFTON','NEVOJAT E PËRDITSHME','m 0 60 b 0 260 260 260 260 60 l 0 60 m 25 0 l 235 0'),(24,26.5,'02','MJAFTUESHMËRIA','PA VARËSI NGA TË TJERËT','m 0 130 l 70 200 l 230 0 l 270 30 l 75 255 l -35 160'),(36,38.5,'03','KËNAQËSIA','ME ATË QË ALLAHU KA CAKTUAR','m 125 240 b -85 100 0 -40 125 50 b 250 -40 335 100 125 240')]
for a,b,n,title,sub,path in cutaways:
 rect(a,b,0,270,1080,1160,'201810',3)
 ev(a,b,'Head',r'{\pos(540,400)\fad(90,90)\fs130\1c&H00E5FF&}'+n,4)
 ev(a,b,'Head',r'{\move(540,600,540,560,0,220)\fad(90,90)\fs54}'+title,4)
 ev(a,b,'Small',r'{\pos(540,1280)\fad(90,90)\fs29\1c&H8AC815&}'+sub,4)
 ev(a,b,'Small',r'{\an5\pos(540,820)\p1\bord0\shad0\1c&H8AC815&\fscx70\fscy70\t(0,260,\fscx100\fscy100)\fad(90,90)}'+path,4)
(p/'captions.ass').write_text(head+'\n'.join(e))
# Synthesize quiet whoosh + low impact accents under the normalized voice.
sr=48000;rng=random.Random(7);samples=[0.0]*math.ceil(duration*sr)
for start in [0,3,7.5,10,16,17,19.5,21,24,26.5,29,33,36,38.5]:
 for i in range(int(.22*sr)):
  t=i/sr;v=.035*math.exp(-t*23)*math.sin(2*math.pi*95*t)+.012*rng.uniform(-1,1)*math.sin(math.pi*t/.22)**2
  j=int(start*sr)+i
  if j<len(samples):samples[j]+=v
# Quiet text clicks on each spoken word, plus short rising transition textures.
for start in word_times:
 for i in range(360):
  j=int(start*sr)+i
  if j<len(samples):samples[j]+=.006*math.exp(-i/65)*math.sin(2*math.pi*1700*i/sr)
for boundary in [3,16,29]:
 for i in range(int(.38*sr)):
  t=i/sr;j=int((boundary-.38)*sr)+i
  if 0<=j<len(samples):samples[j]+=.014*(t/.38)**2*math.sin(2*math.pi*(240*t+1800*t*t))
with wave.open(str(p/'cues.wav'),'w') as w:
 w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(b''.join(struct.pack('<h',int(s*32767)) for s in samples))
f=[]
for i,(a,b) in enumerate(clips):
 f += [f'[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS[v{i}]',f'[0:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS[a{i}]']
f += [''.join(f'[v{i}][a{i}]' for i in range(len(clips)))+f'concat=n={len(clips)}:v=1:a=1[cut][voice]']
f += ["[cut]scale=1080:1640:force_original_aspect_ratio=increase,crop=1080:1640,zoompan=z='if(lt(on,10),1.16-on*0.011,if(eq(mod(floor(on/75),2),0),1.02,1.12))':x='iw/2-iw/zoom/2':y='ih*0.25-ih*0.25/zoom':d=1:s=1080x1640:fps=30,eq=contrast=1.07:saturation=0.88:brightness=-0.008,pad=1080:1920:0:150:color=0x101820,ass=/workspace/video-overhaul/captions.ass[v]"]
f += ['[voice]highpass=f=85,volume=30dB,loudnorm=I=-16:TP=-1.5:LRA=9[clean]','[clean][1:a]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.94[outa]']
(p/'filter.txt').write_text(';'.join(f))
print('Duration:',duration)
