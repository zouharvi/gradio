import os
import unittest

import pytest

import gradio as gr
from gradio import mix
from gradio.external import TooManyRequestsError

"""
WARNING: Some of these tests have an external dependency: namely that Hugging Face's Hub and Space APIs do not change, and they keep their most famous models up.
So if, e.g. Spaces is down, then these test will not pass.
"""

os.environ["GRADIO_ANALYTICS_ENABLED"] = "False"


class TestSeries:
    @pytest.mark.asyncio
    async def test_in_interface(self):
        io1 = gr.Interface(lambda x: x + " World", "textbox", gr.Textbox())
        io2 = gr.Interface(lambda x: x + "!", "textbox", gr.Textbox())
        series = mix.Series(io1, io2)
        assert await series.process(["Hello"]) == ["Hello World!"]

    # @pytest.mark.asyncio
    # @pytest.mark.flaky
    # async def test_with_external(self):
    #     io1 = gr.Interface.load("spaces/abidlabs/image-identity")
    #     io2 = gr.Interface.load("spaces/abidlabs/image-classifier")
    #     series = mix.Series(io1, io2)
    #     try:
    #         output = series("gradio/test_data/lion.jpg")
    #         assert output["lion"] > 0.5
    #     except TooManyRequestsError:
    #         pass


class TestParallel:
    @pytest.mark.asyncio
    async def test_in_interface(self):
        io1 = gr.Interface(lambda x: x + " World 1!", "textbox", gr.Textbox())
        io2 = gr.Interface(lambda x: x + " World 2!", "textbox", gr.Textbox())
        parallel = mix.Parallel(io1, io2)
        assert await parallel.process(["Hello"]) == ["Hello World 1!", "Hello World 2!"]

    @pytest.mark.asyncio
    async def test_multiple_return_in_interface(self):
        io1 = gr.Interface(
            lambda x: (x, x + x), "textbox", [gr.Textbox(), gr.Textbox()]
        )
        io2 = gr.Interface(lambda x: x + " World 2!", "textbox", gr.Textbox())
        parallel = mix.Parallel(io1, io2)
        assert await parallel.process(["Hello"]) == [
            "Hello",
            "HelloHello",
            "Hello World 2!",
        ]

    @pytest.mark.flaky
    def test_with_external(self):
        io1 = gr.Interface.load("spaces/abidlabs/english_to_spanish")
        io2 = gr.Interface.load("spaces/abidlabs/english2german")
        parallel = mix.Parallel(io1, io2)
        try:
            hello_es, hello_de = parallel("Hello")
            assert "hola" in hello_es.lower()
            assert "hallo" in hello_de.lower()
        except TooManyRequestsError:
            pass


if __name__ == "__main__":
    unittest.main()
