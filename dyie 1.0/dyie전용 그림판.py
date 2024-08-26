import tkinter as tk
from tkinter import colorchooser
from tkinter import filedialog

class DyiePaint:
    def __init__(self, master):
        self.master = master
        self.master.title("DYIE 그림판")

        self.canvas = tk.Canvas(master, bg='white', width=500, height=500)
        self.canvas.pack()

        self.button_color = tk.Button(master, text="색상 선택", command=self.choose_color)
        self.button_color.pack(side=tk.LEFT)

        self.button_save = tk.Button(master, text="저장", command=self.save_dyie)
        self.button_save.pack(side=tk.RIGHT)

        self.color = 'black'
        self.canvas.bind("<B1-Motion>", self.paint)

        # 캔버스에 그린 색상을 저장할 배열
        self.pixels = [[(255, 255, 255) for _ in range(500)] for _ in range(500)]

    def choose_color(self):
        color = colorchooser.askcolor()
        if color[1]:
            self.color = color[1]

    def paint(self, event):
        x, y = event.x, event.y
        r = 5  # 브러시 크기
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=self.color, outline=self.color)

        # 색상 배열에 현재 색상 저장
        hex_color = self.canvas.winfo_rgb(self.color)
        rgb_color = (hex_color[0] // 256, hex_color[1] // 256, hex_color[2] // 256)
        for i in range(-r, r+1):
            for j in range(-r, r+1):
                if (i**2 + j**2) <= r**2:  # 원 안에 있는 픽셀만 색상 변환
                    if 0 <= x+i < 500 and 0 <= y+j < 500:
                        self.pixels[y+j][x+i] = rgb_color

    def save_dyie(self):
        # 파일 다이얼로그 열기
        file_path = filedialog.asksaveasfilename(defaultextension=".dyie", filetypes=[("DYIE files", "*.dyie")])
        if file_path:
            self.create_dyie_file(file_path)

    def create_dyie_file(self, file_path):
        width = 500
        height = 500
        # .dyie 파일 생성
        with open(file_path, "wb") as f:
            f.write(b'DYIE')  # 포맷 식별자
            f.write(width.to_bytes(4, 'big'))  # 너비
            f.write(height.to_bytes(4, 'big'))  # 높이

            # 이미지 데이터를 저장
            for y in range(height):
                for x in range(width):
                    r, g, b = self.pixels[y][x]
                    f.write(r.to_bytes(2, 'big'))  # R
                    f.write(g.to_bytes(2, 'big'))  # G
                    f.write(b.to_bytes(2, 'big'))  # B

if __name__ == "__main__":
    root = tk.Tk()
    app = DyiePaint(root)
    root.mainloop()
