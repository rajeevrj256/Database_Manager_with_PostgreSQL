from langchain import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()



llm=OpenAI(api_key=OPENAI_API_KEY)
memory = ConversationBufferMemory()
def define_complexity(prompt):
    template=PromptTemplate(
        
        input_variables=["user_input"],
        template="""Define the complexity (simple or complex) of the following  query prompt of PostgreSQL: '{user_input}'."""
    )
    formatted_prompt=template.format(user_input=prompt,chat_history=memory.buffer)
    
    
    response= llm(formatted_prompt).strip().lower()
    
    memory.save_context({"user_input":prompt},{"response":response})
    return response


def create_new_table(prompt):
    try:
       
        template = PromptTemplate(
            input_variables=["user_input"],
            template="""
            You are an expert PostgreSQL query generator. Write a highly optimized SQL query to create a new table with the following schema:
            {user_input}.
            
            Note: Only Give PostgreSQL Query.Stricly follow the given format.
            """
        )
        formatted_prompt = template.format(
            user_input=prompt,
        )
        response = llm(formatted_prompt)
        return response.strip()

    except Exception as e:
        return f"Error: {e}"
    
    
def generate_query(prompt, table_name, column_names):
    try:
       
        template = PromptTemplate(
            input_variables=["user_input", "table_name", "column_names"],
            template="""You are an expert PostgreSQL query generator. Write a highly optimized SQL query for the following request: 
            '{user_input}' from table '{table_name}' having columns {column_names}, use columns as a string in PostgreSQLquery. 
            Ensure the query is efficient and follows best practices. Generate only one response.
            
            Note: Only Give PostgreSQL Query.Stricly follow the given format.
            """
        )
        formatted_prompt = template.format(
            user_input=prompt,
            chat_history=memory.buffer,
            table_name=table_name,
            column_names=", ".join(column_names)  # Join columns with comma
        )
        response = llm(formatted_prompt)
        memory.save_context({"user_input": prompt}, {"response": response})
        return response.strip()

    except Exception as e:
        return f"Error: {e}"
    
    
def generate_query_with_complex(prompt, table_name, column_names):
    try:
        
        # Corrected 'input_variables' parameter name
        template = PromptTemplate(
            input_variables=["user_input", "table_name", "column_names"],
            template="""
            You are an expert SQL query generator. Write a highly optimized and complex SQL query 
            for the following request: '{user_input}' from table '{table_name}' having columns {column_names}. 
            Include joins, subqueries, grouping, and ordering wherever necessary. 
            Ensure the query is efficient and follows best practices.
            
            Note: Only Give Sql Query.Stricly follow the given format.
            """
        )

        # Formatting the prompt correctly
        formatted_prompt = template.format(
            user_input=prompt,
            table_name=table_name,
            column_names=", ".join(column_names) , # Join columns with comma
            chat_history=memory.buffer
        )

        response = llm(formatted_prompt)
        memory.save_context({"user_input": prompt}, {"response": response})
        return response.strip()

    except Exception as e:
        return f"Error: {e}"
    