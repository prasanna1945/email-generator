import streamlit as st
import google.generativeai as genai

# ----------------------------
# Setup (API Key from secrets)
# ----------------------------
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ----------------------------
# Initialize the model once
# ----------------------------
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config={
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 2048,  # Reduced for faster response
        "response_mime_type": "text/plain",
    },
    system_instruction=(
        "You are an expert email writer. "
        "Create a professional, clear, and engaging email "
        "based on the given key points. Highlight key points in bold."
    ),
)

# ----------------------------
# Email generation function
# ----------------------------
def generate_email_script(sender_name, receiver_name, key_points):
    """Generates a professional email based on sender, receiver, and key points."""
    try:
        prompt = (
            f"Create a professional email from {sender_name} to {receiver_name}.\n\n"
            f"Include the following key points exactly and highlight them in bold:\n{key_points}\n\n"
            "Email:"
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Error generating email: {e}"

# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(page_title="Email Drafting Assistant", page_icon="✉️", layout="wide")

# Custom CSS
st.markdown(
    """
    <style>
        .main-title { 
            color: #4CAF50; 
            text-align: center; 
            font-size: 2.2em; 
            font-weight: bold; 
            margin-bottom: 20px;
        }
        .generated-email {
            background-color: #f9f9f9; 
            color: #111;  /* <-- Added text color */
            padding: 20px; 
            border-radius: 12px; 
            border: 1px solid #ddd; 
            font-family: "Courier New", monospace;
            white-space: pre-wrap;
            line-height: 1.5;
        }
        .download-btn {
            margin-top: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<p class="main-title">✉️ Email Drafting Assistant</p>', unsafe_allow_html=True)

# Sidebar inputs
st.sidebar.header("📌 Email Details")
sender_name = st.sidebar.text_input("Sender's Name", placeholder="e.g., John Doe")
receiver_name = st.sidebar.text_input("Receiver's Name", placeholder="e.g., Jane Smith")
key_points = st.sidebar.text_area(
    "Key Points (one per line)", 
    placeholder="- Introduce project\n- Request meeting\n- Mention deadline"
)

# Generate button
if st.sidebar.button("Generate Email"):
    if sender_name and receiver_name and key_points:
        with st.spinner("✍️ Drafting your email..."):
            script = generate_email_script(sender_name, receiver_name, key_points)

        st.subheader("📨 Generated Email")
        st.markdown(f'<div class="generated-email">{script}</div>', unsafe_allow_html=True)

        st.download_button(
            label="📥 Download Email",
            data=script,
            file_name="email_draft.txt",
            mime="text/plain",
            key="download_email",
        )
    else:
        st.sidebar.error("Please fill in all fields.")
