import yaml
from fastapi import FastAPI
from src.BlogOutline import BlogOutline

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

app = FastAPI()
outline_manager = BlogOutline()


@app.get('/generate_blog')
def generate_blog(topic: str, instructions: str):
    outline = outline_manager.generate_outline(
                                    topic=topic,
                                    instructions=instructions
                                )
    return {'outline': outline}