"""Extract keypoints from a text."""

from dataclasses import dataclass

from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
from pydantic import BaseModel, Field

from keyrag.keypoint.openai_chat_config import OpenAIChatConfig


class Keypoints(BaseModel):
    """Represents keypoints extracted from a text.

    A good keypoint is a very short sentence that captures one aspect of the text.
    The keypoint should be concise and informative.
    """

    keypoints: list[str] = Field(
        ..., description="The keypoints extracted from the text."
    )


DEFAULT_KEYPOINTER_TEMPLATE = """You have a text. \
You are an expert in the field, but you are not pretentious.

Extract at least five keypoints from the text.

The text is: {text}
"""


@dataclass
class Keypointer:
    """Extract keypoints from a text."""

    chat_openai_config: OpenAIChatConfig
    keypointer_template: str = DEFAULT_KEYPOINTER_TEMPLATE

    def __post_init__(self):
        """Initialize the keypointer."""
        self.prompt = ChatPromptTemplate(
            [SystemMessagePromptTemplate.from_template(self.keypointer_template)]
        )
        self.model = self.chat_openai_config.to_model()
        self.structured_llm = self.model.with_structured_output(Keypoints)
        self.chain = self.prompt | self.structured_llm

    def invoke(self, text: str) -> Keypoints:
        """Extract keypoints from a text."""
        output = self.chain.invoke({"text": text})
        if not isinstance(output, Keypoints):
            raise ValueError(f"Unexpected output type: {type(output)}")
        return output
