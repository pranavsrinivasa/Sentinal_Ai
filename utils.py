import os 
from dotenv import load_dotenv
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex,SummaryIndex,SimpleDirectoryReader
from llama_index.core import load_index_from_storage, StorageContext
from llama_index.core.node_parser import (
    SentenceSplitter,
    SemanticSplitterNodeParser,
)
from llama_index.core.agent import ReActAgent
from llama_index.llms.groq import Groq
from llama_index.core.tools import QueryEngineTool,FunctionTool
from llama_index.core.prompts import ChatMessage
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import keras
from tqdm import tqdm
import getlogs

class cyberbot:
    def __init__(self) -> None:

        load_dotenv()
        os.environ['GOOGLE_API_KEY']  = os.getenv('GOOGLE_API_KEY')
        if os.getenv('GOOGLE_API_KEY') != 'YOUR_API_KEY':
            print('API LOADED')
        else:
            print("PLEASE ADD API")
        self.gemma_llm = Gemini(model='models/gemini-1.5-flash',temperature=0.7,max_tokens=200000)
        self.embed_model = embed_model = HuggingFaceEmbedding(model_name='BAAI/bge-small-en-v1.5')
        reader = SimpleDirectoryReader(input_dir="Data")
        self.documents = reader.load_data()
        self.groq_llm = Groq(model="llama3-70b-8192", api_key="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")

        pass

    def create_qe(self):

        
        splitter2 = SentenceSplitter(chunk_size = 2000,chunk_overlap=200)
        nodes2 = splitter2.get_nodes_from_documents(self.documents)

        if not os.path.exists('F:\Devfolio_hack\devfolio_hackathon-Cyber-AI\VectorData'):
            store = VectorStoreIndex(nodes2,embed_model=self.embed_model,show_progress=True)
            store.storage_context.persist(
                persist_dir='F:\Devfolio_hack\devfolio_hackathon-Cyber-AI\VectorData'
            )
        else:
            store = load_index_from_storage(
                            StorageContext.from_defaults(persist_dir=f"F:\Devfolio_hack\devfolio_hackathon-Cyber-AI\VectorData"),
                            embed_model = self.embed_model
                        )
        
        summary_index = SummaryIndex(nodes2)
        self.vqe = store.as_query_engine(llm=self.gemma_llm)
        self.sqe = summary_index.as_query_engine(llm=self.gemma_llm)

        return
    
    def main_agent(self,proompt):
        self.create_qe()
        tools = [QueryEngineTool.from_defaults(name="vector_tool", description="This tool is used to understand specifics about the context",query_engine=self.vqe), QueryEngineTool.from_defaults(query_engine=self.sqe,name="summary_tool",description="This tool provides overall summary about the context")]

        context = """
                Role: CyberSecurity Expert
                Instructions:
                - You are give have the tools vector_tool and summary_tool
                - According to the user query you will either have to create a Cyber Audit Report or provide information about the logs
                - Use the tools to get context and answer the user's query
                - Do not hallucinate context
                - Do not hallucinate user query
                - Do not deviate from the instructions and stick to the role
                - Follow the instructions 
                - Answer in detail to answer the user's query
                - Provide the complete output at the end
                - Provide detailed request as input to the tools
        """

        agent = ReActAgent.from_tools(tools=tools,context=context,llm=self.groq_llm,verbose=True,max_iterations=100)
        res = agent.query(proompt)

        return res.response
    def load_models(self):
        input_layer = keras.layers.Input(shape=(1, 43))

    # LSTM layers
        x = keras.layers.LSTM(128, return_sequences=True,activation='relu')(input_layer)
        x = keras.layers.Dropout(0.2)(x)
        x = keras.layers.LSTM(64, return_sequences=True)(x)
        x = keras.layers.Dropout(0.2)(x)
        x = keras.layers.LSTM(32)(x)
        x = keras.layers.Dropout(0.2)(x)

        # Fully connected Dense layer
        x = keras.layers.Dense(32, activation='relu')(x)

        # Output for binary classification (label)
        label_output = keras.layers.Dense(1, activation='sigmoid', name='label_output')(x)

        # Output for multiclass classification (attack_cat)
        attack_cat_output = keras.layers.Dense(10, activation='softmax', name='attack_cat_output')(x)


        # Train the model
        model_label = keras.Model(inputs=input_layer, outputs=[label_output])
        model_cat = keras.Model(inputs=input_layer, outputs=[attack_cat_output])
        model_label.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        model_cat.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )

        model_cat.load_weights('models\cyber_sec_category.weights.h5')

        model_label.load_weights(filepath='models\cyber_sec_label.weights.h5')

        return model_cat,model_label

    def create_logs(self,input):
        getlogs.main(max_count=1,time_interval=10)
        response = {}
        response['status'] = "NO FILE FOUND, ERRROR"
        response['filename'] = False
        if os.path.exists('Data\cybersecurity_logs_structured.csv'):
            with open('Data\cybersecurity_logs_structured.csv','r') as f:
                res = f.read()
            response['status'] = 'File Created'
            response['filename'] = 'Data\cybersecurity_logs_structured.csv'
        return str(response)
    
    def unstruct_to_csv(self,data):
        read_logs = data
        messages = [ChatMessage(role="system",content="""
        Instructions:
        - From the input data, split into relevant columns and provide output as comma seperated values (csv)
        - The relevant columns from the unstructured data need to created
        - The data from unstructured data need to placed under the relevant columns
        - Ensure that there is a column name for every data column
        - Ensure accurate column names representing the data accurately
        - Do no hallucinate the data
        - Do not change the data from the user input
        - Follow strictly the format of comma seperated values
        - Do not deviate from the instructions
        - Follow the instructions strictly
        Example:
        - Eg1:
        Input: Rajesh from 12 to 1 has created a Agentic RAG pilot
                Pranav from 2 to 3 has completed a Cybersecurity analysis
                Akbhar from 11-12 did a development improvement
                John in the span of 1-5 did got Clients on board
        Output: Name,time,work
                Rajesh,12-1,Agentic Rag pilot
                Pranav,2-3,Cybersecurity analysis
                Akbhar,11-12,Development
                John,1-5, Client Onboarding
        - Eg2: 
        Input:2024-09-22 15:09 Rs134 Rs133 Rs132
            2024-09-23 1:34 Rs1021.1 Rs956 Rs737
            2023-04-22 17:12 Rs1201 Rs420 Rs240
        Output:YYYY-MM-DD,HH:MM,High,Curremt,Low
                2024-09-22,15:09,Rs134,Rs133,Rs132
                2024-09-23,1:34,Rs1021.1,Rs956,Rs737
                2023-04-22,17:12,Rs1201,Rs420,Rs240
    """), ChatMessage(role="user",content=f"The below data given is a set of logs of process of a system, order them in a csv manner, Data: {read_logs}")]
        res = self.gemma_llm.chat(messages)
        return res.message.content
    
    def preprocess(self):
        X = pd.read_csv('UNSW_NB15_training-set.csv')
        label_encoders = {}
        for col in ['proto', 'service', 'state', 'attack_cat']:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col])
            label_encoders[col] = le

        scaler = MinMaxScaler()

        y_cat = X['attack_cat']
        X[X.columns] = scaler.fit_transform(X[X.columns])
        # Normalize numerical columns using MinMaxScaler
        y_label = X['label']
        X = X.drop(columns=['label', 'attack_cat'])

        X = np.array(X)
        X = X.reshape((X.shape[0], 1, X.shape[1])) 
        return X

    def detect_danger(self,input:str)->str:
        encoding = {'Analysis': 0, 'Backdoor': 1, 'DoS': 2, 'Exploits': 3, 'Fuzzers': 4, 'Generic': 5, 'Normal': 6, 'Reconnaissance': 7, 'Shellcode': 8, 'Worms': 9}
        res = {}
        X = self.preprocess()
        model_cat,model_label = self.load_models()
        preds = model_label.predict(X[:1000])
        cats = model_cat.predict(X[:1000])
        with open('LOG_DETECTS.txt','+a') as f:
            for i in tqdm(range(len(preds))):
                pred = 1 if preds[i] > 0.5 else 0
                temp = "Log is Normal\n"
                cat = None
                if pred == 1:
                    for j,k in zip(encoding.values(),encoding.keys()):
                        if j == np.argmax(cats[i]):
                            cat = encoding[k]
                            break
                    temp = f"The log {i} is suspicious with category {k}\n"
                    print(temp)
                f.write(temp)
        reader = SimpleDirectoryReader(input_files=["LOG_DETECTS.txt"])
        documents = reader.load_data()

        splitter2 = SentenceSplitter(chunk_size = 2000,chunk_overlap=200)
        nodes = splitter2.get_nodes_from_documents(documents,show_progress=True)

        summary_index = SummaryIndex(nodes)
        sqe1 = summary_index.as_query_engine(llm=self.gemma_llm)
        res = sqe1.query(input)
        return res.response
    def master_agent(self,query):
        file_expert_tool = FunctionTool.from_defaults(name='file_expert_tool',description="This is a function to retrieve information about files, and to generate whole audit report based on the logs",fn=self.main_agent)
        create_logs_tool = FunctionTool.from_defaults(name='create_logs_tool',description="This tool is used to create logs from the existing computer and saves it in a file",fn=self.create_logs)
        detect_danger_tool = FunctionTool.from_defaults(name='detect_danger_tool',description="This tool that checks logs, detects danger ans query according to the input, it takes only one input of the type string",fn=self.detect_danger)
        context1 = """
            Role: CyberSecurity Expert
            Instructions:
            - You have the tools detect_danger_tool,file_expert_tool and create_logs_tool
            - Use file_expert_tool tool to get insights from the existing data
            - Get insigths and the audit report from file_expert_tool and generate a final cohesive report with valid information
            - Ensure all the user queries are answered in the answer
            - Use create_logs_tool to generate logs from the existing computer
            - Provide a complete answer with all the information gained in previous steps
            - Do not hallucinate context
            - Do not deviate from instructions
            - Do not use create_logs_tool unless specified by the user
            - Provide complete instructions for the file_expert_tool
            - Use detect_danger_tool to get information about dangerous or suspicious logs
            - Follow the user query strictly
        """
        master_agent = ReActAgent.from_tools(tools = [create_logs_tool,file_expert_tool,detect_danger_tool],context=context1,llm=self.gemma_llm,max_iterations=50,verbose=True)
        res = master_agent.query(query)

        return res.response