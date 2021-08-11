import os, glob, time
from os import listdir
from os.path import isfile, join

def list_file():
	n=1
	print("\n[List Folder]")
	der=[f for f in listdir("result")]
	for d in der:
		print(f"{n}. {d}")
		n+=1
	pil=int(input("pilih: "))
	return der[pil-1]

def isi_file(der):
	n=1
	print(f"\n[List File: {der}]")
	isi=glob.glob(f"result/{der}/*.pdf")
	for i in isi:
		print(f"{n}. {i.split('/')[-1:][0]}")
		n+=1
	return isi

os.system("clear")
print("\n[program ini untuk memudahkan kamu membaca hasil convert-an LiNoid]\n")
lst=list_file()
while True:
	isi=isi_file(lst)
	lih=input("[ketik \"B\" untuk kembali ke list folder]\npilih: ")
	if lih.lower() == "b":
		os.system("clear")
		print("\n[program ini untuk memudahkan kamu membaca hasil convert-an LiNoid]\n")
		lst=list_file()
	elif lih.isdigit():
		print(f"[membuka file {isi[int(lih)-1].split('/')[-1:][0]}]")
		time.sleep(1)
		os.system(f"xdg-open '{isi[int(lih)-1]}'")


