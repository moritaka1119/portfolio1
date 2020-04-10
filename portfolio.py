from pathlib import Path
import os, tkinter, tkinter.filedialog, tkinter.messagebox
from PIL import Image
from pdf2image import convert_from_path
import sys
import pyocr
import re
# ファイル選択、ファイルのパスを習得
root = tkinter.Tk()
root.withdraw()
fTyp = [("","*")]
iDir = os.path.abspath(Path().resolve())
tkinter.messagebox.showinfo('ファイル選択','pdf または写真ファイルを選択してください！')
file = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)

# 処理ファイル名表示
tkinter.messagebox.showinfo('実行','OCRを実行します')

# OCRツールが使えるか確認
tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found　---- OCRツールが呼び出せません。")
    sys.exit(1)

tool = tools[0]

# ファイルのパスを引き継ぐ
input_file = file

# pdfの場合は写真に変更して実行、写真の場合は写真で実行
texts = []
if '.pdf' in input_file:
    pages = convert_from_path(input_file)
    for page in pages:
        txt = tool.image_to_string(
            page,
            lang="jpn",
            builder=pyocr.builders.TextBuilder(tesseract_layout=3)
        )
        texts.append(txt)
    
else:
    try:
        txt = tool.image_to_string(
        Image.open(input_file),
        lang="jpn",
        builder=pyocr.builders.TextBuilder(tesseract_layout=3)
         )
        texts.append(txt)
        
# pdfまたは写真以外のファイルを選択するとエラーメッセージを表示し、実行をやめる
    except OSError:
        tkinter.messagebox.showinfo("エラー", "pdf または写真以外のフォルダーが選択されています。フォルダー選択からやり直してください。")
        sys.exit()

# 出力
new_texts = []      
for txt in texts:
    txt_list = txt.split("\n")
    for t in txt_list:
        if t != " " and t != "":
            new_texts.append(t)
            new_texts.append("\n")
texts = new_texts
file_name = file.split(".")[0].split("/")[-1]
txts = "".join(texts)
path = file_name + ".txt"
with open( path, mode = "w") as f:
    f.write(txts)
