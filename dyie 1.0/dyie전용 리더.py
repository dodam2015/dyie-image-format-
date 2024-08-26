import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class DyieReader:
    def __init__(self, master):
        self.master = master
        self.master.title("DYIE 리더")

        self.canvas = tk.Canvas(master, bg='white', width=500, height=500)
        self.canvas.pack()

        self.button_open = tk.Button(master, text="열기", command=self.open_dyie)
        self.button_open.pack()

    def open_dyie(self):
        file_path = filedialog.askopenfilename(filetypes=[("DYIE files", "*.dyie")])
        if file_path:
            self.load_dyie_file(file_path)

    def load_dyie_file(self, file_path):
        with open(file_path, "rb") as f:
            # 파일 헤더 읽기
            identifier = f.read(4)
            if identifier != b'DYIE':
                print("잘못된 DYIE 파일입니다.")
                return
            
            width = int.from_bytes(f.read(4), 'big')
            height = int.from_bytes(f.read(4), 'big')

            # 이미지 데이터 읽기
            image_data = []
            for y in range(height):
                row = []
                for x in range(width):
                    r = int.from_bytes(f.read(2), 'big')
                    g = int.from_bytes(f.read(2), 'big')
                    b = int.from_bytes(f.read(2), 'big')
                    row.append((r, g, b))  # RGB 값 저장
                image_data.append(row)

            # 이미지 생성
            self.display_image(image_data, width, height)

    def display_image(self, image_data, width, height):
        # PIL을 사용하여 이미지 생성
        image = Image.new("RGB", (width, height))
        for y in range(height):
            for x in range(width):
                # RGB 값 설정
                image.putpixel((x, y), image_data[y][x])
        
        # Tkinter 캔버스에 이미지 표시
        self.tk_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = DyieReader(root)
    root.mainloop()
