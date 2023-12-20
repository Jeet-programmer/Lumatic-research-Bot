import pprint
import os
import google.generativeai as palm

api_key = ""
palm.configure(api_key="")

def get_text_model_list():
    models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
    model = models[0].name
    return model

text_model = get_text_model_list()
print("Using Text Generation Model as ", text_model)

def get_response(prompt, model=text_model, max_output_token=600, temperature=0.4, top_p=0.95, top_k=40):
    prompt = prompt

    completion = palm.generate_text(
        model=model,
        prompt=prompt,
        max_output_tokens=max_output_token, 
        temperature=temperature, 
        top_p=top_p, 
        top_k=top_k
    )

    return completion

def get_embedding_model_list():
    for model in palm.list_models():
        if 'embedText' in model.supported_generation_methods:
            return model

embedding_model = get_embedding_model_list()
print("Using Text Generation Model as ", embedding_model.name)

def get_embeddings(text):
    text = text

    # Create an embedding
    embeddings = palm.generate_embeddings(model=embedding_model, text=text)

    return embeddings['embedding']

if __name__ == "__main__":
    get_text_model_list()
    get_response()
    get_embedding_model_list()
    get_embeddings()
