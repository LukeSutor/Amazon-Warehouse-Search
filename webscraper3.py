from tkinter import *
import tkinter as tk
import requests
from bs4 import BeautifulSoup
import re
import keyboard

class webscraperApp(tk.Tk):
  def __init__(self):
    tk.Tk.__init__(self)
    self.title("Amazon Warehouse Search")
    self.geometry("700x500")
    # Create and add search label
    self.search_label = tk.Label(font=("Calibre", 16), text="Enter search term")
    self.search_label.pack()

    # Create and add search entry
    self.search_entry = tk.Entry(width=30)
    self.search_entry.pack()

    # Create and add keyword labels
    self.keyword_label_1 = tk.Label(font=("Calibre", 16), text="Enter keywords for search term")
    self.keyword_label_1.pack()
    self.keyword_label_2 = tk.Label(font=("Calibre", 10), text="Format keywords as capitalized phrases separated by commas. (No spaces) \nex. Large,Green,Empty")
    self.keyword_label_2.pack()

    # Create and add keyword entry
    self.keyword_entry = tk.Entry(width=50)
    self.keyword_entry.pack()

    # Create and add submit button
    self.button = tk.Button(text="Search", command=self.webscraper)
    self.button.pack()

    # Create scrollbar
    self.sb = tk.Scrollbar(self)
    self.sb.pack(side = RIGHT, fill = Y)

    # Create listbox for all labels
    self.label_listbox = tk.Listbox(self, yscrollcommand = self.sb.set, width=100, height=50)

  def webscraper(self):
    # Extract search string from window
    search = self.search_entry.get()
    # Extract keywords string from windo and use split() to turn it into an array
    keywordString = self.keyword_entry.get()
    keywords = keywordString.split(',')
    print(keywords)
    self.label_listbox.insert(END, "Search results for " + search + ":" + "\n")
    self.sb.config(command = self.label_listbox.yview)  
    self.label_listbox.pack()
    for i in range(1, 14):
      self.label_listbox.insert(END, "Page " + str(i) + "\n")
      # url formatter that takes in search for the search term and page for the page number
      url = 'https://www.amazon.com/s?k={search}&i=warehouse-deals&page={page}'.format(search=search, page=i)
      headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Chrome/41.0.2228.0 Safari/537.36', }
      page = requests.post(url, headers=headers)

      # if the page is responsive, complete the rest of the script
      if page.status_code == 200:
        # retrieve all html data from the webpage
        pageText = BeautifulSoup(page.text, 'html.parser')
        # get all h2 html tags from the html data
        saleLabels = pageText.find_all("h2")
        # if there are no h2 tags (there always should be h2 tags) repeat previous code until there are h2 tags
        while not saleLabels:
          page = requests.post(url, headers=headers)
          pageText = BeautifulSoup(page.text, 'html.parser')
          saleLabels = pageText.find_all("h2")

        for label in saleLabels:
          # find the tag that contains the link to the product if you can
          try:
            link = label.find("a")["href"]
          except:
            pass
          # find all the product labels on the page
          label = label.find("span").text

          for word in keywords:
            if re.search(word, label) is not None:
              self.label_listbox.insert(END, label + "\n")
              self.label_listbox.insert(END, "https://amazon.com" + link + "\n")
              self.label_listbox.insert(END, "\n")


ws = webscraperApp()
ws.mainloop()