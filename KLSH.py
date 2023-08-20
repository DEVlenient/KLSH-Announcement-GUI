import tkinter as tk
from tkinter import ttk
import urllib.request as req
import bs4

def fetch_announcements(index):
    request = req.Request(url)
    
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    root = bs4.BeautifulSoup(data, "html.parser")
    
    div_all = root.find_all("div", class_="wp-block-buttons")
    strong = div_all[index].strong.string.strip()
    
    ul_all = root.find_all("ul", class_="wp-block-latest-posts__list has-dates wp-block-latest-posts")
    content = ul_all[index]
    
    li_all = content.find_all("li")
    announcements = []
    for li in li_all:
        a_all = li.find("a")
        title = a_all.get_text()
        link = a_all["href"]
        announcements.append((title, link))
    
    return strong, announcements

def update_announcements():
    selected_index = category_combobox.current()
    if selected_index >= 0:
        strong, announcements = fetch_announcements(selected_index)
        result_label.config(text=strong)
        
        text_widget.delete(1.0, tk.END)
        for title, link in announcements:
            text_widget.tag_configure("link", foreground="blue", underline=True)
            text_widget.insert(tk.END, title, "link")
            text_widget.insert(tk.END, "\n\n")
            text_widget.tag_bind("link", "<Enter>", lambda e: text_widget.config(cursor="hand2"))
            text_widget.tag_bind("link", "<Leave>", lambda e: text_widget.config(cursor=""))
            text_widget.tag_bind("link", "<Button-1>", lambda e, link=link: link_clicked(link))

def link_clicked(link):
    import webbrowser
    webbrowser.open_new_tab(link)

url = "https://www.klsh.kl.edu.tw/"

# 建立主視窗
root = tk.Tk()
root.title("國立基隆高級中學 KLSH 公告查詢")
root.geometry("800x600")

# 建立選單
category_label = tk.Label(root, text="選擇公告類別：")
category_label.pack()

categories = ["置頂", "重要"]
category_combobox = ttk.Combobox(root, values=categories)
category_combobox.pack()

update_button = tk.Button(root, text="查詢", command=update_announcements)
update_button.pack()

# 顯示結果
result_label = tk.Label(root, text="", font=("Helvetica", 16))
result_label.pack()

text_widget = tk.Text(root, wrap=tk.WORD, width=70, height=25)
text_widget.pack()

root.mainloop()
