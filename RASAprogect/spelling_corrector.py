from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.constants import TEXT
from textblob import TextBlob
from typing import Any, Dict, List


@DefaultV1Recipe.register(
    component_types=[GraphComponent], is_trainable=False
)
class SpellingCorrector(GraphComponent):
    """Custom component to correct spelling errors using TextBlob."""

    def __init__(self, config: Dict[str, Any]) -> None:
        self.name = "spelling_corrector"

    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        return {}

    def process(self, messages: List[Message]) -> List[Message]:
        for message in messages:
            original_text = message.get(TEXT)
            if original_text:
                corrected_text = str(TextBlob(original_text).correct())
                
                print(f"[SpellingCorrector] Original: '{original_text}' --> Corrected: '{corrected_text}'")
                message.set(TEXT, corrected_text)
        return messages

    @classmethod
    def create(
        cls,
        config: Dict[str, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ) -> "SpellingCorrector":
        return cls(config)
