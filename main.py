import tkinter as tk
from tkinter import ttk
import webbrowser
import requests
import json


def search_videos():
    query = search_entry.get()
    if not query.strip():
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Please enter a search query")
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

        result_text.delete(1.0, tk.END)
        for r in results:
            result_dict = json.loads(r["_src_"])
            print(result_dict)
            video_id = result_dict['id']['videoId']
            r = result_dict["snippet"]
            title = r['title']
            url = f"https://www.youtube.com/watch?v={video_id}"

            result_text.insert(tk.END, f"{title}\n", "title")
            result_text.insert(tk.END, f"{url}\n", "url")
    #             result_text.insert(tk.END, f"{url}\n", "url")
    except requests.RequestException as e:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"An error occurred: {str(e)}")


def open_url(event):
    start_index = result_text.index(f"@{event.x},{event.y} linestart")
    end_index = result_text.index(f"@{event.x},{event.y} lineend")
    url = result_text.get(start_index, end_index)
    webbrowser.open(url)


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

result_text = tk.Text(main_frame, wrap=tk.WORD, width=50, height=15)
result_text.grid(column=1, row=1, columnspan=2, sticky=(tk.W, tk.E))

result_text.tag_configure("url", foreground="blue", underline=1)
result_text.tag_bind("url", "<Enter>", lambda e: result_text.config(cursor="hand2"))
result_text.tag_bind("url", "<Leave>", lambda e: result_text.config(cursor=""))
result_text.tag_bind("url", "<Button-1>", open_url)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.rowconfigure(1, weight=1)

root.mainloop()
