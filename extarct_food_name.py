import os
import keys as key
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

os.environ['OPENAI_API_KEY'] = key.openai_api_key

llm = OpenAI(temperature=0.3)

def generate_restaurant_name_and_item(cuisines):
    prompt_temp_name = PromptTemplate(
        input_variables=['cuisines'],
        template="{cuisines} give me all the food names from above list food without any descriptors"
    )


    name_chain = LLMChain(
        llm=llm,
        prompt=prompt_temp_name,
        output_key='food_name')

    prompt_temp_item = PromptTemplate(
        input_variables=['food_name'],
        template="{food_name} , Give this output in comma seprated from"
    )

    item_chain = LLMChain(
        llm=llm, 
        prompt=prompt_temp_item,
        output_key='food_items'
        )
    chain = SequentialChain(
        chains=[name_chain,item_chain],
        input_variables = ['cuisines'],
        output_variables = ['food_name','food_items'])

    return chain({'cuisines':cuisines})

