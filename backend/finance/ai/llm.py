from openai import OpenAI
from django.conf import settings

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=settings.HF_API_KEY,
)


def call_llama(prompt: str) -> str:
    """
    Calls Llama 3.1 via Hugging Face router.
    """

    completion = client.chat.completions.create(
        model="meta-llama/Llama-3.1-8B-Instruct:novita",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=512,
        temperature=0.2,
    )

    return completion.choices[0].message.content
