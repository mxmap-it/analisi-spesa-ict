import zipfile,re,sys,glob,html
def xlsx(p):
  z=zipfile.ZipFile(p); ss=[]
  if "xl/sharedStrings.xml" in z.namelist():
    for si in re.findall(r"<si>(.*?)</si>",z.read("xl/sharedStrings.xml").decode(),re.S):
      ss.append(html.unescape("".join(re.findall(r"<t[^>]*>(.*?)</t>",si,re.S))))
  wbx=z.read("xl/workbook.xml").decode(); names=re.findall(r"<sheet [^>]*name=\"([^\"]+)\"",wbx)
  out=""
  for i,sh in enumerate(sorted([n for n in z.namelist() if re.match(r"xl/worksheets/sheet\d+\.xml",n)],key=lambda s:int(re.findall(r"\d+",s)[0]))):
    out+=f"=== foglio {names[i] if i<len(names) else sh}\n"
    for row in re.findall(r"<row[^>]*>(.*?)</row>",z.read(sh).decode(),re.S):
      v=[]
      for attrs,body in re.findall(r"<c([^>]*?)(?:/>|>(.*?)</c>)",row,re.S):
        m=re.search(r"<v>(.*?)</v>",body or ""); t=re.search(r"<t[^>]*>(.*?)</t>",body or "",re.S)
        if "t=\"s\"" in attrs and m: v.append(ss[int(m.group(1))])
        elif m: v.append(m.group(1))
        elif t: v.append(html.unescape(t.group(1)))
      v=[x.strip() for x in v if x and x.strip()]
      if v: out+=" | ".join(v)+"\n"
  return out
def docx(p): return html.unescape(re.sub(r"<[^>]+>"," ",zipfile.ZipFile(p).read("word/document.xml").decode().replace("</w:p>","\n")))
D="../t62_testi/"
for t in glob.glob(D+"*.txt"):
  if open(t).read().startswith("ERRORE"):
    b=t[:-4]+".bin"
    try: s=xlsx(b)
    except Exception:
      s=docx(b)
    open(t,"w",encoding="utf-8").write(s)
