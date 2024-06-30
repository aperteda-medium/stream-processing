from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from openai import OpenAI

# import time
import json

router = APIRouter()
client = OpenAI()

@router.get("/openai-stream-response")
def openai_stream_response():
    def event_stream_iterator(stream):
        for chunk in stream:
            print('first chunk = ')

            for choice in chunk.choices:
                stream_data_chunk = choice.delta.content
                if stream_data_chunk != None:
                    yield "id: test\n" + "event: my_custom_event\n" + "data: " + stream_data_chunk + "\n\n"

    openai_response_stream = client.chat.completions.create(
      model="gpt-4o",
      stream=True,
      messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What are in these images? Is there any difference between them?",
                },
                 {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
                    },
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
                    },
                },
            ],
        }
    ],
      max_tokens=300,
  )


    return StreamingResponse(
        event_stream_iterator(openai_response_stream),
        media_type="text/event-stream"
    )

@router.get("/openai-normal-response")
def open_api_normal_response():
    openai_normal_response = client.chat.completions.create(
          model="gpt-4o",
          messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What are in these images? Is there any difference between them?",
                    },
                     {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
                        },
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
                        },
                    },
                ],
            }
        ],
          max_tokens=300,
    )

    print('openai_normal_response = ', openai_normal_response)
    print('openai_normal_response.choices[0] = ', openai_normal_response.choices[0].message.content)

    return json.dumps({
        "message": openai_normal_response.choices[0].message.content
    })