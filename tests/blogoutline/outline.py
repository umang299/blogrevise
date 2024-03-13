import os
import sys
import unittest
from unittest.mock import patch, MagicMock

cwd = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(cwd)

from backend.src.aws import AWSClient
from backend.src.utils import load_yaml_file
from backend.src.BlogOutline import BlogOutline


config = load_yaml_file(
                    file_path=os.path.join(
                                        cwd,
                                        'backend',
                                        'config.yaml'
                                    )
                )

outline_client = BlogOutline()
aws_client = AWSClient(config=config)


class TestGenerate(unittest.TestCase):
    def test_outline_generator(self):
        topic = 'AI'
        instructions = 'Keep it under 100 words'
        outline = outline_client.generate_outline(
                                        topic=topic,
                                        instructions=instructions)
        self.assertEqual(type(outline), str)

    def test_user_outlines(self):
        user_id = 'abc123456'
        files = outline_client.get_outline_filenames_by_user_id(
                                    user_id=user_id
                                )
        self.assertEqual(type(files), list)

    def test_save(self):
        text = 'Test Upload'
        status, filename = aws_client.upload_file(
                                        text=text,
                                        filename='testupload.txt'
                                    )
        self.assertEqual(status, True)
        self.assertEqual(filename, 'testupload.txt')


if __name__ == '__main__':
    unittest.main()
