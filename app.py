import time
from fpdf import FPDF
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage


# Page config
st.set_page_config(page_title="Chatbot", layout="wide")

# Sidebar
st.sidebar.title("⚙️ Setup")

# Hidden API key input
api_key = st.sidebar.text_input(
    "Gemini API Key",
    type="password",  # hides text
    placeholder="Enter your Gemini API key..."
)

model_name = st.sidebar.selectbox("Select Model", ["gemini-pro", "gemini-2.0-flash"])
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)

# Setup button
if "is_setup" not in st.session_state:
    st.session_state.is_setup = False

if st.sidebar.button("Setup"):
    if api_key:
        try:
            llm = ChatGoogleGenerativeAI(
                model=model_name,
                temperature=temperature,
                api_key=api_key
            )
            
            # 🔹 Test initialization with a small dummy request
            test_msg = "Hello! Test message."
            _ = llm.invoke(test_msg)  # will raise if API key or model invalid
            
            # If we reach here, it's working
            st.session_state.llm = llm
            st.session_state.is_setup = True
            st.sidebar.success("✅ Setup complete! You can start chatting.")
        
        except Exception as e:
            st.sidebar.error(f"❌ Model initialization failed: {e}")
            st.session_state.is_setup = False
            st.session_state.llm = None
    else:
        st.sidebar.error("⚠️ Please enter your Gemini API key first.")


# --- Chat history download button ---
def create_pdf(chat_history):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    
    for msg in chat_history:
        if isinstance(msg, HumanMessage):
            role = "User"
        elif isinstance(msg, AIMessage):
            role = "Assistant"
        else:
            continue  # Skip SystemMessage
        # role = "User" if isinstance(msg, HumanMessage) else "Assistant"
        pdf.multi_cell(0, 8, f"{role}: {msg.content}")
        pdf.ln(1)
    
    pdf_output = "chat_history.pdf"
    pdf.output(pdf_output)
    return pdf_output

# Disable button if no chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [
        SystemMessage(content="You are a helpful assistant"),
    ]

if st.sidebar.button("📄 Download Chat History as PDF"):
    pdf_file = create_pdf(st.session_state.chat_history)
    with open(pdf_file, "rb") as f:
        st.sidebar.download_button(
            label="Download PDF",
            data=f,
            file_name="chat_history.pdf",
            mime="application/pdf",
        )



# Main chat window
st.title("💬 Chatbot")


if not st.session_state.is_setup:
    st.info("⚙️ Please complete setup from the sidebar to start chatting.")
else:
    # Initialize messages
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = [
            SystemMessage(content="You are a helpful assistant"),
        ]

    # Mapping classes to roles (skip system)
    role_map = {
        HumanMessage: "user",
        AIMessage: "assistant"
    }

    # Print messages skipping SystemMessage
    for msg in st.session_state.chat_history:
        if type(msg) in role_map:
            role = role_map[type(msg)]
            with st.chat_message(role):
                st.markdown(msg.content)
            # print(f"{role}: {msg.content}")

    # Display past messages
    # for msg in st.session_state.messages:
    #     with st.chat_message(msg["role"]):
    #         st.markdown(msg["content"])

    # Input box
    if prompt := st.chat_input("Type your message..."):
        # Save user message
        # st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state["chat_history"].append(HumanMessage(content=prompt))
        with st.chat_message("user"):
            st.markdown(prompt)

        # bot response
        response = st.session_state.llm.invoke(st.session_state["chat_history"]).content
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state["chat_history"].append(AIMessage(content=response))

        # print(st.session_state["messages"])
        print(st.session_state["chat_history"])

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            displayed_text = ""
            for char in response:
                displayed_text += char
                message_placeholder.markdown(displayed_text + "▌")
                time.sleep(0.03)
            message_placeholder.markdown(response)


        # with st.chat_message("assistant"):
        #     st.markdown(response)




