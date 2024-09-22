import os
import tkinter as tk
from openai import OpenAI
from dotenv import load_dotenv
from tkinter import filedialog, ttk, messagebox

load_dotenv()

client = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))


# Function to list all text files in a specified folder
def list_text_files(folder_path):
    return [f for f in os.listdir(folder_path) if f.endswith('.txt')]

# Function to read the contents of a file
def read_file_contents(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read file '{file_path}': {e}")
        return ""

# Class to create the custom UI
class FileRelationshipApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Relationship Creator")

        # Choose folder button
        self.folder_btn = tk.Button(root, text="Choose Folder", command=self.choose_folder)
        self.folder_btn.grid(row=0, column=0, padx=10, pady=10)
        
        self.folder_label = tk.Label(root, text="No folder selected.")
        self.folder_label.grid(row=0, column=1, padx=10, pady=10)

        # Add relationship button
        self.add_relationship_btn = tk.Button(root, text="Add Relationship", command=self.add_relationship_slot)
        self.add_relationship_btn.grid(row=1, column=0, padx=10, pady=10)
        self.add_relationship_btn["state"] = "disabled"  # Disabled until folder is chosen

        # Submit relationships button
        self.submit_btn = tk.Button(root, text="Submit Relationships", command=self.submit_relationships)
        self.submit_btn.grid(row=1, column=1, padx=10, pady=10)
        self.submit_btn["state"] = "disabled"  # Disabled until folder is chosen

        # Frame to hold the relationship slots
        self.slot_frame = tk.Frame(root)
        self.slot_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.files = []
        self.file_paths = {}
        self.relationship_slots = []

    # Function to choose folder
    def choose_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.files = list_text_files(folder_path)
            if not self.files:
                messagebox.showerror("Error", "No .txt files found in the selected folder.")
                return

            # Store the file paths
            for file in self.files:
                self.file_paths[file] = os.path.join(folder_path, file)

            self.folder_label.config(text=f"Selected Folder: {os.path.basename(folder_path)}")
            self.add_relationship_btn["state"] = "normal"
            self.submit_btn["state"] = "normal"

    # Function to add a relationship slot
    def add_relationship_slot(self):
        slot = {}

        # Dropdown 1 (file selection)
        slot['file1'] = ttk.Combobox(self.slot_frame, values=self.files, state="readonly")
        slot['file1'].grid(row=len(self.relationship_slots), column=0, padx=5, pady=5)
        slot['file1'].set("Select File 1")

        # Text entry for relationship
        # slot['relationship'] = tk.Entry(self.slot_frame)
        # slot['relationship'].grid(row=len(self.relationship_slots), column=1, padx=5, pady=5)
        # slot['relationship'].insert(0, "Type of relationship")

        # Dropdown 1 (file selection)
        slot['relationship'] = ttk.Combobox(self.slot_frame, values=['WORKED FOR', 'LOVED', 'HAD KILLED', 'MURDERED FOR', 'POOPED IN', 'SHARED WITH'], state="readonly")
        slot['relationship'].grid(row=len(self.relationship_slots), column=1, padx=5, pady=5)
        slot['relationship'].set("Type of relationship")

        # Dropdown 2 (file selection)
        slot['file2'] = ttk.Combobox(self.slot_frame, values=self.files, state="readonly")
        slot['file2'].grid(row=len(self.relationship_slots), column=2, padx=5, pady=5)
        slot['file2'].set("Select File 2")

        # Append the slot to the list
        self.relationship_slots.append(slot)

    # Function to submit relationships and send to OpenAI API
    def submit_relationships(self):
        relationships = []
        
        for slot in self.relationship_slots:
            file1 = slot['file1'].get()
            file2 = slot['file2'].get()
            relationship = slot['relationship'].get()

            # Ensure valid inputs
            if file1 == "Select File 1" or file2 == "Select File 2" or not relationship:
                messagebox.showwarning("Invalid Input", "Please complete all fields.")
                return

            file1_content = read_file_contents(self.file_paths[file1])
            file2_content = read_file_contents(self.file_paths[file2])
            
            relationships.append((file1_content, relationship, file2_content))

        # Display the natural language conversion of relationships
        natural_language_output = self.convert_relationships_to_natural_language(relationships)
        if natural_language_output:
            messagebox.showinfo("Natural Language Output", natural_language_output)

    # Function to convert relationships to natural language using OpenAI API
    def convert_relationships_to_natural_language(self, relationships):
        meanings = []
        connections = ''

        for relationship in relationships:
            connections += f"{relationship[0]}\n{relationship[1].upper()}\n{relationship[2]}\n\n"
        print(f'Connections: {connections}')

        try:
            # Call OpenAI API
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": [
                            {
                            "type": "text",
                            "text": "You are to work on a fun and absurd conspiracy creator game. The player is presented with a list of things like notes, news snippets, images and location markers. They can then connect them in any order with some relationship between the connections. This final conspiracy is to be judged and scored to rank the player on a global leaderboard. You'll be presented with 2 clues connected with a relationship. Combine the meaning of the 2 based on the relationship provided and explain in a single short paragraph."
                            }
                        ]
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                            "type": "text",
                            "text": connections
                            }
                        ]
                    }
                ],
                temperature=0.4,
                max_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            meaning = response.choices[0].message.content
            meanings.append(meaning)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to contact OpenAI API: {e}")
            return None

        # Join meanings into a single string, each meaning separated by a newline
        total_meaning = "\n".join(meanings)
        print(f"Total meaning\n{total_meaning}\n")
        return total_meaning


if __name__ == "__main__":
    root = tk.Tk()
    app = FileRelationshipApp(root)
    root.mainloop()
