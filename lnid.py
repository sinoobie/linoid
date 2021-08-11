import requests, re, os, time, sys
from fpdf import FPDF
from bs4 import BeautifulSoup as BS

class PDF(FPDF):
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Dejavu italic 8
        self.set_font('DejaVu', '', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'R')

    def print_chapter(self, text):
        self.add_page()
        # Dejavu 12
        self.set_font('DejaVu', '', 12)
        # Output justified text
        self.multi_cell(0, 5, text)
        # Line break
        self.ln()

def download(url, cap, title):
	MAINPATH=f"result/{title}"
	try:
		os.mkdir(MAINPATH)
	except: pass

	try:
		req=requests.get(url)
		bs=BS(req.text, "html.parser")
		txt=bs.find("div",{"class":"text-left"})

		text=""
		for x in txt.find_all("p"):
			text+=x.text.strip()+"\n\n"
		
		pdf = PDF()
		pdf.add_font('DejaVu','','DejaVuSansCondensed.ttf', uni=True)
		PATH=f"{MAINPATH}/{cap}"
		pdf.print_chapter(text)
		pdf.output(f"{PATH}.pdf", "F")
		return True
	except KeyboardInterrupt:
		sys.exit()
	except:
		return False

def chap_dl(cap, pilih, title):
	if "-" in pilih:
		pilih=pilih.split("-")
		if len(pilih) == 2 and pilih[1] != "":
			ran=range(int(pilih[0]), int(pilih[1])+1)
		else:
			ran=range(int(pilih[0]), len(cap)+1)

		for x in ran:
			proges=f"[*] Converting {cap[x-1]['cap']} to pdf"
			print(f"\r{proges}",end="",flush=True)
			dl=download(cap[x-1]["url"], cap[x-1]['cap'], title)
			while dl != True:
				print(f"\r{' '*len(proges)}",end="", flush=True)
				print(f"\r[x] Gagal {cap[x-1]['cap']}",end="",flush=True)
				time.sleep(1)
				print(f"\r[@] Mengulangi {cap[x-1]['cap']}",end="",flush=True)
				dl=download(cap[x-1]["url"], cap[x-1]['cap'], title)
			else:
				print(f"\r{' '*len(proges)}",end="", flush=True)
				print(f"\r[✓] Berhasil {cap[x-1]['cap']}",end="",flush=True)
				print()
	else:
		proges=f"[*] Converting {cap[int(pilih)-1]['cap']} to pdf"
		print(f"\r{proges}",end="",flush=True)
		dl=download(cap[int(pilih)-1]["url"], cap[int(pilih)-1]['cap'], title)
		while dl != True:
			print(f"\r{' '*len(proges)}",end="", flush=True)
			print(f"\r[x] Gagal {cap[int(pilih)-1]['cap']}",end="",flush=True)
			time.sleep(1)
			print(f"\r[@] Mengulangi {cap[int(pilih)-1]['cap']}",end="",flush=True)
			dl=download(cap[int(pilih)-1]["url"], cap[int(pilih)-1]['cap'], title)
		else:
			print(f"\r{' '*len(proges)}",end="", flush=True)
			print(f"\r[✓] Berhasil {cap[int(pilih)-1]['cap']}",end="",flush=True)
			print()

def get_chap(url):
	_cap=[]
	_req=requests.get(url)
	mid=re.findall("data-id=\"(.*?)\"", _req.text)
	req=requests.post("https://meionovel.id/wp-admin/admin-ajax.php", data={"action":"manga_get_chapters", "manga":mid})
	bs=BS(req.text, "html.parser")
	data=bs.find("ul", {"class":"sub-chap list-chap"})
	while data == None:
		get_chap(url)

	n=0
	for x in data.find_all("li"):
		nc=x.find("a").text.strip()
		_cap.append([n, nc, x.find("a")["href"]])
		n-=1
	_cap.sort()

	hasil=[{"cap":y[1], "url":y[2]} for y in _cap]
	return hasil

def cari(query):
	result=[]
	req=requests.get(f"https://meionovel.id/?s={query}&post_type=wp-manga")
	if "No matches found. Try a different search..." in req.text:
		return 0
	bs=BS(req.text, "html.parser")
	items=bs.find("div",{"class":"c-tabs-item"})
	if items == None:
		cari(query)

	title=items.find_all("h3", {"class":"h4"})	
	for t in title:
		jsn={"title":t.text, "url":t.find("a")["href"]}
		result.append(jsn)
	return result

try:
	os.mkdir("result")
except: pass

try:
	os.system("clear")
	print("""\033[97m
        [ LiNoid (Light Novel id) ]
                - noobie -         
""")
	query=input("Cari: ")
	hasil=cari(query)
	if len(hasil) > 1:
		n=1
		for x in hasil:
			print(f"{n}. {x['title']}")
			n+=1
		pil=int(input("Pilih: "))
		lih=hasil[pil-1]["url"]
		title=hasil[pil-1]["title"]
	elif len(hasil) == 1:
		lih=hasil[0]["url"]
		title=hasil[0]["title"]
	else:
		print("!¡ light novel tidak tersedia ¡!")
		sys.exit()

	print(f"\n\033[96m[•{title}•]")
	_req=requests.get(lih)
	_bs=BS(_req.text, "html.parser")
	_gen=_bs.find("div",{"class":"genres-content"})
	_rate=_bs.find("div", {"typeof":"AggregateRating"}).text.strip()
	print(f"[•Genre: {_gen.text.strip()}•]\n[•Rating: {' '.join(_rate.split()[-7:])}•]")
	cap=get_chap(lih)
	for y in range(len(cap)):
		print(f"[{y+1}] {cap[y]['cap']}")
	print(f"""[ {len(cap)} (Total) Chapter ditemukan ]

\033[97m[info]
# ketik (misalnya: 10-) untuk mendownload dari nomor 10 sampai akhir
# ketik (misalnya: 10-20) untuk mendownload dari nomor 10 sampai 20
# ketik angka saja tanpa garis untuk mendownload salah satu""")
	pilih=input("noobie/> ")
	chap_dl(cap, pilih, title)
except Exceptiona as err:
	print(err)