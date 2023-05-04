import openai
from RPA.Robocorp.Vault import Vault

_secret = Vault().get_secret("OpenAI")

def message(role: str, content: str):
    return {"role": role, "content": content}

def call_openai(prompt: str, temperature=0.0, llm_model="gpt-3.5-turbo",
                echo_user_prompt=False, echo_response=True) -> str:
    if echo_user_prompt:
        print(prompt)
    openai.api_key = _secret["key"]
    print("<OpenAI> Calling OpenAI")
    completion = openai.ChatCompletion.create(
        model=llm_model,
        messages=[
            message(
                "system",
                "You are an assistant for extracting structured data from email conversations.",
            ),
            message("user", prompt),
        ],
        temperature=temperature,
    )
    choice = completion.choices[0]  # type: ignore
    if echo_response:
        try:
            print(f'{choice["message"]["content"]}\n```')
        except:
            print(repr(completion))
    print("<OpenAI> Got response")
    print(f"""<OpenAI> Tokens spent: {completion["usage"]["total_tokens"]} """)  # type: ignore
    return choice["message"]["content"]