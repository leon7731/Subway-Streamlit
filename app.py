
import streamlit as st

import subway_api_func as saf
import mapping_func as mf

# Plot 
from streamlit_folium import st_folium


# LLM
import os
from langchain_community.document_loaders import CSVLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI
from langchain_openai import OpenAIEmbeddings

st.title('Subway Location App')


### Part 1: Subway Location Map ###
@st.cache_data
def get_subway_data():
    jwt_token = saf.Login(Email = st.secrets["email"], 
                Password = st.secrets["password"], 
                URL = 'http://50.19.149.26/auth/login')


    subway_info_data = saf.extract_subway_info_data(JWT_Token=jwt_token)
    return subway_info_data

# Fetch and cache subway data
subway_info_data = get_subway_data()
    

subway_info_map = mf.create_folium_map(subway_info_data)
st_folium(subway_info_map, width=1000, height=500)




### Part 2: Chatbot ###

st.title("Chat App")

os.environ['OPENAI_API_KEY'] = st.secrets["openai_api_key"]

# Cached function to load documents and create index

def load_documents_and_create_index():
    loader = CSVLoader(file_path='geocoded_subway_locations.csv')
    index_creator = VectorstoreIndexCreator()
    docsearch = index_creator.from_loaders([loader])
    chain = RetrievalQA.from_chain_type(llm=OpenAI(temperature=0), 
                                        chain_type="stuff", 
                                        retriever=docsearch.vectorstore.as_retriever(), 
                                        input_key="question")
    return chain

# # Load the documents and create index with a spinner
# with st.spinner('Loading data, please wait...'):
chain = load_documents_and_create_index()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask any Subway Information related Question?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get response from chain
    response = chain.invoke({"question": prompt})
    response = response['result']
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})