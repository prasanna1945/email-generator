import streamlit as st
import google.generativeai as genai

def generate_email_script(sender_name, receiver_name, key_points):
    """Generates an email script based on the given sender, receiver, and key points.

    Args:
        sender_name: The name of the email sender.
        receiver_name: The name of the email receiver.
        key_points: The key points for the email.

    Returns:
        The generated email script.
    """
    try:
        # Configure API key
        genai.configure(api_key="AIzaSyAnKEhsyH4tYpjBFSFmi7zTY2lpeWE7tpk")

        # Create the model
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            system_instruction="You are an expert email writer. Create a professional and engaging email script based on the given key points.",
        )

        # Construct the prompt
        prompt = (f"Create a professional email based on these key points:\n{key_points}\n\n"
                  f"The email should be from {sender_name} to {receiver_name}.\n\nEmail:")

        # Generate the email script
        response = model.generate_content(prompt)
        email_text = response.text

        # Highlight the key points in the generated email
        for point in key_points.split('\n'):
            email_text = email_text.replace(point, f"<strong>{point}</strong>")

        return email_text
    except Exception as e:
        return f"Error: {e}"

# Streamlit application
st.set_page_config(page_title="Email Drafting Assistant", page_icon="✉️")

st.markdown("""
    <style>
    .title {
        color: #4CAF50;
        text-align: center;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Email Drafting Assistant ✉️")

st.write("""
    Welcome to the Email Drafting Assistant! This tool helps you create professional and engaging email drafts 
    based on the key points you provide. Simply enter the sender's name, receiver's name, and key points, and let our AI generate the email for you!
""")

sender_name = st.text_input("Enter the sender's name:", help="The name of the person sending the email.")
receiver_name = st.text_input("Enter the receiver's name:", help="The name of the person receiving the email.")
key_points = st.text_area("Enter the key points for the email:", help="Provide the key points you want to include in the email, each on a new line.")

if st.button("Generate Email"):
    if sender_name and receiver_name and key_points:
        with st.spinner("Generating your email..."):
            script = generate_email_script(sender_name, receiver_name, key_points)
        st.subheader("Generated Email:")
        st.markdown(script, unsafe_allow_html=True)
    else:
        st.error("Please enter the sender's name, receiver's name, and the key points.")
