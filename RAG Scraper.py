import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import bs4 as bs
import requests
import configparser
import os
from langchain_community.document_loaders import WebBaseLoader, PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_ollama.llms import OllamaLLM


class RAGApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("RAG Scraper AI")
        self.geometry("1000x800")
        self.resizable(False, True)

        # Initialize config
        self.config_file = "settings.ini"
        self.config = configparser.ConfigParser()
        self.load_config()

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)  # Updated to account for new frame

        # Get available Ollama models
        self.available_models = self.get_available_models()

        # Loader type selection
        self.loader_frame = ctk.CTkFrame(self)
        self.loader_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.loader_label = ctk.CTkLabel(
            self.loader_frame, text="Select Loader Type:")
        self.loader_label.pack(side="left", padx=5)

        saved_loader = self.config.get(
            'Settings', 'loader_type', fallback="Web Loader")
        self.loader_type = ctk.CTkOptionMenu(
            self.loader_frame,
            values=["Web Loader", "PDF Loader"],
            command=self.on_loader_change
        )
        self.loader_type.set(saved_loader)
        self.loader_type.pack(side="left", padx=5)

        # Model selection frame
        self.model_frame = ctk.CTkFrame(self)
        self.model_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Base model selection
        self.model_label = ctk.CTkLabel(
            self.model_frame, text="Base Model:")
        self.model_label.pack(side="left", padx=5)

        saved_model = self.config.get(
            'Settings', 'model_type', fallback="llama2")
        self.model_type = ctk.CTkOptionMenu(
            self.model_frame,
            values=self.available_models if self.available_models else [
                "llama2"],
            command=self.on_model_change
        )
        self.model_type.set(saved_model if saved_model in (
            self.available_models if self.available_models else ["llama2"]) else "llama2")
        self.model_type.pack(side="left", padx=5)

        # Embeddings model selection
        self.embeddings_label = ctk.CTkLabel(
            self.model_frame, text="Embeddings Model:")
        self.embeddings_label.pack(side="left", padx=5)

        saved_embeddings = self.config.get(
            'Settings', 'embeddings_model', fallback="all-minilm")
        self.embeddings_type = ctk.CTkOptionMenu(
            self.model_frame,
            values=self.available_models if self.available_models else [
                "all-minilm"],
            command=self.on_embeddings_change
        )
        self.embeddings_type.set(saved_embeddings if saved_embeddings in (
            self.available_models if self.available_models else ["all-minilm"]) else "all-minilm")
        self.embeddings_type.pack(side="left", padx=5)

        # Source frames
        # PDF frame
        self.pdf_frame = ctk.CTkFrame(self)
        self.pdf_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.pdf_label = ctk.CTkLabel(self.pdf_frame, text="PDF Source:")
        self.pdf_label.pack(side="left", padx=5)

        self.pdf_entry = ctk.CTkEntry(self.pdf_frame, width=400)
        self.pdf_entry.pack(side="left", padx=5, fill="x", expand=True)

        self.browse_button = ctk.CTkButton(
            self.pdf_frame,
            text="Browse",
            command=self.browse_file
        )
        self.browse_button.pack(side="right", padx=5)
        self.pdf_frame.grid_remove()  # Hidden by default

        # Web frame for URLs and BS4 strainer
        self.web_frame = ctk.CTkFrame(self)
        self.web_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.web_frame.grid_columnconfigure(1, weight=1)

        # URLs section
        self.url_label = ctk.CTkLabel(
            self.web_frame, text="URLs (one per line):")
        self.url_label.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

        self.url_text = ctk.CTkTextbox(self.web_frame, width=400, height=100)
        self.url_text.grid(row=1, column=0, columnspan=2,
                           padx=5, pady=5, sticky="ew")

        # BS4 strainer section
        self.bs4_label = ctk.CTkLabel(
            self.web_frame, text="BS4 Strainer Class(enter class name of the element of your target page to narrow down the context area):")
        self.bs4_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.bs4_entry = ctk.CTkEntry(self.web_frame, width=200)
        self.bs4_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.bs4_entry.insert(0, "")  # Default value

        # Question frame
        self.question_frame = ctk.CTkFrame(self)
        self.question_frame.grid(
            row=3, column=0, padx=10, pady=10, sticky="ew")  # Updated row position

        self.question_label = ctk.CTkLabel(
            self.question_frame, text="Question:")
        self.question_label.pack(side="left", padx=5)

        self.question_entry = ctk.CTkEntry(self.question_frame, width=400)
        self.question_entry.pack(side="left", padx=5, fill="x", expand=True)

        # Process button
        self.process_button = ctk.CTkButton(
            self.question_frame,
            text="ASK AI",
            command=self.process_query
        )
        self.process_button.pack(side="right", padx=5)

        # Answer text area
        self.answer_frame = ctk.CTkFrame(self)
        self.answer_frame.grid(row=4, column=0, padx=10,
                               pady=10, sticky="nsew")
        self.answer_frame.grid_columnconfigure(0, weight=1)
        self.answer_frame.grid_rowconfigure(1, weight=1)

        self.answer_label = ctk.CTkLabel(self.answer_frame, text="Answer:")
        self.answer_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.answer_text = ctk.CTkTextbox(
            self.answer_frame, width=900, height=400)
        self.answer_text.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        if self.loader_type.get() == "PDF Loader":
            # set all pdf loader element to shown and hide all web loader elements
            self.pdf_frame.grid()
            self.web_frame.grid_remove()
        else:
            # set all web loader elements to shown and hide all pdf loader elements
            self.pdf_frame.grid_remove()
            self.web_frame.grid()

    def load_config(self):
        """Load settings from config file"""
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
        if 'Settings' not in self.config:
            self.config['Settings'] = {
                'loader_type': 'Web Loader',
                'model_type': 'llama2',
                'embeddings_model': 'all-minilm'
            }
            self.save_config()

    def save_config(self):
        """Save current settings to config file"""
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def get_available_models(self):
        try:
            response = requests.get(
                'http://localhost:11434/api/tags', timeout=5)  # Add timeout
            if response.status_code == 200:
                models = response.json()
                return [model['name'] for model in models['models']]
            self.show_warning(
                "Ollama API Error", "Could not fetch models from Ollama API. Please make sure Ollama is running.")
            return []
        except requests.exceptions.RequestException as e:
            self.show_warning(
                "Ollama API Error", "Could not connect to Ollama API. Please make sure Ollama is running.")
            print(f"Error fetching models: {str(e)}")
            return []

    def show_warning(self, title, message):
        warning_window = ctk.CTkToplevel(self)
        warning_window.title(title)
        warning_window.geometry("400x150")
        warning_window.transient(self)  # Set to be on top of the main window

        # Center the window
        warning_window.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - \
            (warning_window.winfo_width() // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - \
            (warning_window.winfo_height() // 2)
        warning_window.geometry(f"+{x}+{y}")

        # Add message
        label = ctk.CTkLabel(warning_window, text=message, wraplength=350)
        label.pack(padx=20, pady=20)

        # Add OK button
        ok_button = ctk.CTkButton(
            warning_window, text="OK", command=warning_window.destroy)
        ok_button.pack(pady=10)

        # Make the window modal
        warning_window.grab_set()

    def on_loader_change(self, choice):
        if choice == "PDF Loader":
            self.web_frame.grid_remove()
            self.pdf_frame.grid()
        else:
            self.pdf_frame.grid_remove()
            self.web_frame.grid()

        # Save the new choice
        self.config['Settings']['loader_type'] = choice
        self.save_config()

    def on_model_change(self, choice):
        self.selected_model = choice
        # Save the new choice
        self.config['Settings']['model_type'] = choice
        self.save_config()

    def on_embeddings_change(self, choice):
        self.selected_embeddings = choice
        # Save the new choice
        self.config['Settings']['embeddings_model'] = choice
        self.save_config()

    def browse_file(self):
        filename = filedialog.askopenfilename(
            filetypes=[("PDF files", "*.pdf")]
        )
        if filename:
            self.pdf_entry.delete(0, tk.END)
            self.pdf_entry.insert(0, filename)

    def process_query(self):
        try:
            # Clear previous answer
            self.answer_text.delete("0.0", tk.END)
            self.answer_text.insert("0.0", "Processing...\n")
            self.update()

            # Get loader type and question
            loader_type = self.loader_type.get()
            question = self.question_entry.get()
            selected_model = self.model_type.get()  # Get the selected model
            # Get the selected embeddings model
            selected_embeddings = self.embeddings_type.get()

            # Initialize loader based on type
            if loader_type == "Web Loader":
                # Get URLs from text area (split by newlines and remove empty lines)
                urls = [url.strip() for url in self.url_text.get(
                    "0.0", tk.END).split('\n') if url.strip()]
                if not urls:
                    raise ValueError("Please enter at least one URL")

                # Get BS4 strainer class
                strainer_class = self.bs4_entry.get().strip()
                if not strainer_class:
                    strainer_class = None

                bs4_strainger = bs.SoupStrainer(class_=strainer_class)
                loader = WebBaseLoader(
                    web_paths=urls,
                    bs_kwargs={"parse_only": bs4_strainger}
                )
            else:
                pdf_path = self.pdf_entry.get().strip()
                if not pdf_path:
                    raise ValueError("Please select a PDF file")
                loader = PyMuPDFLoader(pdf_path)

            # Process documents
            docs = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1200,
                chunk_overlap=100,
                add_start_index=True
            )
            all_splits = text_splitter.split_documents(docs)

            # Create vectorstore with selected embeddings model
            local_embeddings = OllamaEmbeddings(model=selected_embeddings)
            vectorstore = Chroma.from_documents(
                documents=all_splits,
                embedding=local_embeddings
            )

            # Retrieve relevant documents
            retriever = vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 3}
            )
            retrieved_docs = retriever.invoke(question)
            context = ' '.join([doc.page_content for doc in retrieved_docs])

            # Generate response using selected model
            llm = OllamaLLM(model=selected_model)
            response = llm.invoke(
                f"Answer the question according to the context: \nQuestion: {
                    question}\n Context: {context}"
            )

            # Display response
            self.answer_text.delete("0.0", tk.END)
            self.answer_text.insert("0.0", response)

        except Exception as e:
            self.answer_text.delete("0.0", tk.END)
            self.answer_text.insert("0.0", f"Error: {str(e)}")


if __name__ == "__main__":
    app = RAGApp()
    app.after(0, lambda:app.state('zoomed'))
    app.mainloop()
