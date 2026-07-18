import json

from openai import OpenAI

def get_weather(city):
    return f"The weather in {city} is sunny and 75°F."

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

function_tools = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "Get the current weather for a city.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city name."
                }
            },
            "required": ["city"]
        }
    }
]

messages = [
    {"role": "developer", "content": "You are a creative storyteller. Write a short story based on the given prompt."},
]

while True:
    prompt = input("Enter your prompt (or 'exit' to quit): ")
    if prompt.lower() == "exit":
        break

    messages.append({"role": "user", "content": prompt})

    response = client.responses.create(
        model="llama3.2:3b",
        input=messages,
        tools=function_tools
    )

    messages.append({"role": "assistant", "content": response.output_text})

    for item in response.output:
        if item.type == "function_call" and item.name == "get_weather":

            weather = get_weather(json.loads(item.arguments)["city"])

            messages.append({
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": weather
            })

            response = client.responses.create(
                model="llama3.2:3b",
                instructions=f"Continue the story with the weather information: {weather}",
                input=messages,
                tools=function_tools
            )


    print(response.output_text)
                 




