
import os
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# 1. Initialize Azure AI Foundry client
client = OpenAI(
    base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"]
)

deployment = os.environ["AZURE_OPENAI_DEPLOYMENT"]
weather_api_key = os.environ["OPENWEATHER_API_KEY"]


# 2. Define the weather tool
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name, for example Bhopal"
                    }
                },
                "required": ["location"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
]


# 3. Implement the actual weather API function
def get_weather(location):
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": location,
        "appid": weather_api_key,
        "units": "metric"
    }

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()

    data = response.json()

    return {
        "city": data["name"],
        "temperature_celsius": data["main"]["temp"],
        "feels_like_celsius": data["main"]["feels_like"],
        "humidity_percent": data["main"]["humidity"],
        "weather_condition": data["weather"][0]["description"],
        "wind_speed_mps": data["wind"]["speed"]
    }


# 4. Ask the model and execute its selected tool
def main():
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful weather assistant. "
                "Use the weather tool for current weather questions. "
                "Base your answer on the tool result."
            )
        },
        {
            "role": "user",
            "content": "How is the weather in bangalore?"
        }
    ]

    response = client.chat.completions.create(
        model=deployment,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=0.3
    )

    assistant_message = response.choices[0].message

    # 5. Check whether the model requested a tool
    if not assistant_message.tool_calls:
        print(assistant_message.content)
        return

    messages.append(
        assistant_message.model_dump(exclude_none=True)
    )

    # 6. Execute each requested tool
    for tool_call in assistant_message.tool_calls:
        if tool_call.function.name == "get_weather":
            arguments = json.loads(
                tool_call.function.arguments
            )

            location = arguments["location"]
            print(f"Fetching current weather for: {location}")

            try:
                weather_data = get_weather(location)

                tool_result = {
                    "success": True,
                    "weather": weather_data
                }

            except requests.RequestException as error:
                tool_result = {
                    "success": False,
                    "error": str(error)
                }

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(tool_result)
            })

    # 7. Send the tool result back to the model
    final_response = client.chat.completions.create(
        model=deployment,
        messages=messages,
        temperature=0.3
    )

    print("\nWeather assistant:")
    print(final_response.choices[0].message.content)


if __name__ == "__main__":
    main()
