from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from secret_key import openapi_key

# Initialize the OpenAI model
llm = OpenAI(model_name="gpt-3.5-turbo-instruct", temperature=0.6, openai_api_key=openapi_key)

def recommend_games(preferences: str) -> list[str]:
    """
    Recommend a list of games based on user preferences.

    Parameters:
    preferences (str): A description of the kind of games the user likes.

    Returns:
    list: list of recommended games
    """
    
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