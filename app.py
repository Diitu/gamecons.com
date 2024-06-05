import streamlit as st
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from secret_key import openapi_key

# Initialize the OpenAI model
llm = OpenAI(model_name="gpt-3.5-turbo-instruct", temperature=0.6, openai_api_key=openapi_key)

def recommend_games(preferences: str) -> list[str]:
    prompt_template_games = PromptTemplate(
        input_variables=['preferences'],
        template="""Based on the following preferences: {preferences}, 
                    suggest top 5 games that the user might enjoy. 
                    Return it as a comma-separated list."""
    )
    
    game_chain = LLMChain(llm=llm,
                          prompt=prompt_template_games,
                          output_key='game_recommendations')

    chain = SequentialChain(
        chains=[game_chain],
        input_variables=['preferences'],
        output_variables=['game_recommendations']
    )
    
    response = chain({'preferences': preferences})
    return response['game_recommendations'].split(', ')

st.title("Game Recommendation AI")

preferences = st.text_area("Enter your game preferences (e.g., genres, features you like):")

if st.button("Get Recommendations"):
    if preferences:
        game_recommendations = recommend_games(preferences)  # Use actual API response
        st.write("Recommended Games:")
        for game in game_recommendations:
            st.write(f"- {game}")
    else:
        st.write("Please enter your game preferences.")