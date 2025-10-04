from dotenv import load_dotenv
import os
import json
import requests
from pypdf import PdfReader
import gradio as gr
import google.generativeai as genai


load_dotenv(override=True)

class Me:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

        self.model = genai.GenerativeModel("gemini-2.5-flash")  # or "gemini-1.5-pro"
        self.name = "Pawee Indulakshana"

        # load linkedin text
        reader = PdfReader("me/pawee.pdf")
        self.linkedin = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin += text

        # load summary
        with open("me/summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read()

    def system_prompt(self):
        system_prompt = f"You are acting as {self.name}. You are answering questions on {self.name}'s website, \
particularly questions related to {self.name}'s career, background, skills and experience. \
Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
You are given a summary of {self.name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "

        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n## LinkedIn Profile:\n{self.linkedin}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt

    def chat(self, message, history):
        full_history = [{"role": "user", "parts": [self.system_prompt()]}]
        for h in history:
            full_history.append({"role": "user", "parts": [h[0]]})
            full_history.append({"role": "model", "parts": [h[1]]})
        full_history.append({"role": "user", "parts": [message]})
    
        response = self.model.generate_content(
            full_history,
        )
                
        return response.text
    

if __name__ == "__main__":
    me = Me()
    gr.ChatInterface(me.chat).launch()
