import google.generativeai as genai
import json
import csv
import tkinter as tk
from tkinter import scrolledtext


genai.configure(api_key=" PASTE YOUR FREE API KEY ")
model = genai.GenerativeModel("gemini-1.5-flash")


def summarize_topic(topic, sentences):
    response = model.generate_content(
        f"Act as a senior content creator and Summarize {topic} into exactly {sentences} sentences with nice flow, clarity, comparing it with its properties in a structured manner and less repetitive."
    )
    return response.text.replace(". ", " ")  # Ensure sentences are not strictly separated into paragraphs


def generate_instagram_titles(topic):
    response = model.generate_content(
        f"Generate catchy and short Instagram titles with emojis for {topic}."
    )
    return response.text


def explain_for_kids(topic):
    response = model.generate_content(
        f"Explain {topic} in a way that a 10-year-old would understand."
    )
    return response.text


def identify_mistakes(text):
    response = model.generate_content(
        f"Analyze the following text and identify any mistakes, inconsistencies, or areas for improvement:\n\n{text}"
    )
    return response.text


def highlight_key_points(text):
    keywords = ["important", "key", "notable", "significant", "critical", "essential"]
    for word in keywords:
        text = text.replace(word, f"**{word.upper()}**")
    return text


def display_output(text):
    output_box.delete(1.0, tk.END)
    text = highlight_key_points(text)
    formatted_text = text.replace(". ", " ")  # Adjust line spacing without strict paragraph breaks
    output_box.insert(tk.END, formatted_text)
    word_count_label.config(text=f"Word Count: {len(text.split())}")


def on_submit(sentences):
    topic = topic_entry.get()
    summary = summarize_topic(topic, sentences)
    display_output(summary)


def regenerate():
    sentences = int(current_sentences.get())
    on_submit(sentences)


def show_instagram_titles():
    topic = topic_entry.get()
    titles = generate_instagram_titles(topic)
    display_output(titles)


def explain_simply():
    topic = topic_entry.get()
    explanation = explain_for_kids(topic)
    display_output(explanation)


def check_mistakes():
    text = output_box.get(1.0, tk.END).strip()
    if text:
        mistakes = identify_mistakes(text)
        display_output(mistakes)


def minimize_to_bubble():
    root.withdraw()
    bubble.deiconify()


def restore_from_bubble():
    bubble.withdraw()
    root.deiconify()


def start_move(event):
    bubble.x = event.x
    bubble.y = event.y


def stop_move(event):
    bubble.x = None
    bubble.y = None


def on_motion(event):
    x = bubble.winfo_x() + (event.x - bubble.x)
    y = bubble.winfo_y() + (event.y - bubble.y)
    bubble.geometry(f"60x60+{x}+{y}")


# GUI Setup
root = tk.Tk()
root.title("Gemini Study Tool")
root.geometry("900x700")
root.configure(bg="#282c34")
root.state('zoomed')  # Open in full-screen mode


# Topic Entry
frame = tk.Frame(root, bg="#282c34")
frame.pack(pady=10)

topic_label = tk.Label(frame, text="Enter the topic:", font=("Times New Roman", 16), fg="white", bg="#282c34")
topic_label.pack(side=tk.LEFT, padx=10)

topic_entry = tk.Entry(frame, font=("Times New Roman", 16), width=50)
topic_entry.pack(side=tk.LEFT, padx=10)


# Sentence Buttons
button_frame = tk.Frame(root, bg="#282c34")
button_frame.pack(pady=10)
current_sentences = tk.StringVar(value="10")

for s in [1, 5, 10, 100]:
    tk.Button(button_frame, text=f"{s}s", font=("Times New Roman", 14, "bold"), bg="#0078D7", fg="white", command=lambda s=s: (current_sentences.set(s), on_submit(s))).pack(side=tk.LEFT, padx=5)


# Action Buttons
action_frame = tk.Frame(root, bg="#282c34")
action_frame.pack(pady=10)

tk.Button(action_frame, text="Regenerate", font=("Times New Roman", 14, "bold"), bg="#FFA500", fg="white", command=regenerate).pack(side=tk.LEFT, padx=5)
tk.Button(action_frame, text="Instagram Titles", font=("Times New Roman", 14, "bold"), bg="#FF4500", fg="white", command=show_instagram_titles).pack(side=tk.LEFT, padx=5)
tk.Button(action_frame, text="Simple Explanation", font=("Times New Roman", 14, "bold"), bg="#32CD32", fg="white", command=explain_simply).pack(side=tk.LEFT, padx=5)
tk.Button(action_frame, text="Identify Mistakes", font=("Times New Roman", 14, "bold"), bg="#DC143C", fg="white", command=check_mistakes).pack(side=tk.LEFT, padx=5)


# Output Box
# Output Box
output_box = scrolledtext.ScrolledText(
    root, wrap=tk.WORD, width=100, height=20,
    font=("Times New Roman", 14), padx=10, pady=10,
    spacing1=10, spacing2=5,
    bg="black",  # Fully black background
    fg="white",  # White text for contrast
    borderwidth=0,  # Removes borders
    highlightthickness=0  # Removes focus highlight
)
output_box.pack(pady=20)



# Word Count Label
word_count_label = tk.Label(root, text="Word Count: 0", font=("Times New Roman", 12), fg="white", bg="#282c34")
word_count_label.pack(side=tk.LEFT, padx=20, pady=10)


# Minimize Button
minimize_button = tk.Button(root, text="Minimize", font=("Times New Roman", 14), bg="gray", fg="white", command=minimize_to_bubble)
minimize_button.pack(pady=5)


# Floating Bubble Window
bubble = tk.Toplevel()
bubble.geometry("60x60+50+50")  # Smaller size
bubble.overrideredirect(True)
bubble.configure(bg="#0078D7")

bubble_label = tk.Label(bubble, text="📚", font=("Times New Roman", 20), fg="white", bg="#0078D7")
bubble_label.pack(expand=True, fill=tk.BOTH)
bubble_label.bind("<Button-1>", lambda e: restore_from_bubble())

# Enable dragging for bubble
bubble.bind("<ButtonPress-1>", start_move)
bubble.bind("<ButtonRelease-1>", stop_move)
bubble.bind("<B1-Motion>", on_motion)

bubble.withdraw()


# Run GUI
root.mainloop()
