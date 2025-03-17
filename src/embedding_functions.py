# This file imports the raw text along with each text's respective category. This assumes the user
# has already downloaded the file and saved it in the './../data/raw/' folder.

import os
import openai
import tiktoken
import dotenv

dotenv.load_dotenv()


# establish OpenAI session
client = openai.OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)


def truncate_text(text, max_tokens=8192, encoding_name="cl100k_base"):
    """
    Truncates the text to a maximum number of tokens using the tiktoken library.

    Example usage:

    df['truncated_text'] = df['text'].apply(lambda t: truncate_text(t, max_tokens=8192))
    """

    encoding = tiktoken.get_encoding(encoding_name=encoding_name)

    tokens = encoding.encode(text)

    if len(tokens) <= max_tokens:
        return(text)
    else:
        # Truncate tokens to max_tokens
        truncated_tokens = tokens[:max_tokens]
        text = encoding.decode(truncated_tokens)
    
    return text


def get_embedding(text):

    final_text = truncate_text(text)

    response = client.embeddings.create(input=final_text, model="text-embedding-3-large")

    return response.data[0].embedding


