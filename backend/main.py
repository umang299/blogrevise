import os
import yaml
from uuid import uuid4
from fastapi import FastAPI

from src.aws import AWSClient
from src.utils import load_yaml_file, save_json_file
from src.BlogOutline import BlogOutline

config = load_yaml_file(file_path='config.yaml')

app = FastAPI()
outline_manager = BlogOutline()
aws_manager = AWSClient(config=config)


@app.get('/generate_blog')
async def generate_blog(topic: str, instructions: str):
    outline = outline_manager.generate_outline(
                                    topic=topic,
                                    instructions=instructions
                                )

    result = {'topic': topic,
              'instructions': instructions,
              'outline': outline}

    filename = save_json_file(
                        data=result,
                        filename=os.path.join(
                                os.getcwd(), 'data', f'{uuid4()}.json')
                    )

    return {
        'outline': outline,
        'filename': filename
        }


@app.post("/upload_to_s3")
async def upload_to_s3(text, filename):
    status, saved_filename = aws_manager.upload_file(
                                            text=text,
                                            filename=filename
                                        )
    if status:
        return {
            'status': status,
            'filename': saved_filename
        }
    else:
        return {'status': status}
