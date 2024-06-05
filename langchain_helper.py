import os
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain

# Initialize the OpenAI model using the API key from the environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("No OpenAI API key found in environment variables.")

llm = OpenAI(model_name="gpt-3.5-turbo-instruct", temperature=0.6, openai_api_key=openai_api_key)

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

# Example usage
if __name__ == "__main__":
    preferences = "I like open-world games with a strong storyline and character development."
    game_recommendations = recommend_games(preferences)  # Use actual API response
    print("Recommended Games:", game_recommendations)
