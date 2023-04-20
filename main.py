import tkinter as tk
from tkinter import ttk
import requests
import json

def search_videos():
    query = search_entry.get()
    if not query.strip():
        result_text.set("Please enter a search query")
        return

    solr_url = "http://localhost:8983/solr/tech_products/select"
    params = {
        "q": query,
        "rows": 10,
        "wt": "json"
    }
    try:
        response = requests.get(solr_url, params=params)
        response.raise_for_status()
        data = response.json()

        results = data["response"]["docs"]

        display_str = ""
        for result in results:
            result_dict = json.loads(result["_src_"])
            display_str += result_dict["snippet"]["title"]
            display_str += "\n"
            display_str += "\n"
        result_text.set(display_str)
    except requests.RequestException as e:
        result_text.set(f"An error occurred: {str(e)}")


root = tk.Tk()
root.title("YouTube Video Search")

main_frame = ttk.Frame(root, padding="10")
main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

search_label = ttk.Label(main_frame, text="Search:")
search_label.grid(column=0, row=0, sticky=tk.W)

search_entry = ttk.Entry(main_frame, width=40)
search_entry.grid(column=1, row=0, sticky=(tk.W, tk.E))

search_button = ttk.Button(main_frame, text="Search", command=search_videos)
search_button.grid(column=2, row=0, sticky=tk.E)

result_label = ttk.Label(main_frame, text="Results:")
result_label.grid(column=0, row=1, sticky=(tk.W, tk.N))

result_text = tk.StringVar()
result_display = ttk.Label(main_frame, textvariable=result_text, anchor=tk.W, justify=tk.LEFT, wraplength=400)
result_display.grid(column=1, row=1, columnspan=2, sticky=(tk.W, tk.E))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.rowconfigure(1, weight=1)

root.mainloop()
