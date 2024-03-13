import yaml
from fastapi import FastAPI

from src.aws import AWSClient
from src.BlogOutline import BlogOutline

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

app = FastAPI()
outline_manager = BlogOutline()
aws_manager = AWSClient(config=config)


@app.get('/generate_blog')
async def generate_blog(topic: str, instructions: str):
    outline = outline_manager.generate_outline(
                                    topic=topic,
                                    instructions=instructions
                                )
    return {'outline': outline}


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
