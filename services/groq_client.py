import os
from groq import Groq
from dotenv import load_dotenv

# Load .env
load_dotenv()

# ✅ CREATE CLIENT HERE
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_groq(prompt):
    try:
        print("Calling Groq...")

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",   # safer model
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        print("Groq success!")
        return response.choices[0].message.content

    except Exception as e:
        print("❌ GROQ ERROR:", str(e))
        return f"ERROR: {str(e)}"