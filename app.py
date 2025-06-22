import streamlit as st
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnableParallel

# ---- LLM setup ----
llm = HuggingFaceEndpoint(
    repo_id='HuggingFaceH4/zephyr-7b-beta',
    task='text-generation',
    huggingfacehub_api_token="########"
)
model = ChatHuggingFace(llm=llm)
parser = StrOutputParser()

# ---- Prompt templates ----
prompt1 = PromptTemplate(
    template='Generate short and simple notes from the following text:\n{text}',
    input_variables=['text']
)

prompt2 = PromptTemplate(
    template='Generate 5 short questions from the following text:\n{text}',
    input_variables=['text']
)

# ---- LangChain pipelines ----
notes_chain = prompt1 | model | parser
quiz_chain = prompt2 | model | parser

# ---- Streamlit UI ----
st.title("📘 Notes & Quiz Generator")

user_text = st.text_area("Enter your educational text here:", height=250)

if st.button("Generate Notes & Quiz"):
    if user_text.strip() == "":
        st.warning("Please enter some text to generate notes and quiz.")
    else:
        with st.spinner("Generating..."):
            notes_result = notes_chain.invoke({'text': user_text})
            quiz_result = quiz_chain.invoke({'text': user_text})

            st.subheader("📝 Generated Notes")
            st.text(notes_result)

            st.subheader("❓ Generated Quiz")
            st.text(quiz_result)

# Optional: Footer
st.markdown("---")
st.caption("Made by Abdul Mukit with 💡 LangChain + Hugging Face")
