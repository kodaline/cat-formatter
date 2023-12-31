from cat.mad_hatter.decorators import tool, hook, plugin
from pydantic import BaseModel, Field
from cat.log import log

class MySettings(BaseModel):
    separator: str = Field(
        title="Sentence formatter",
        description="Choose formatter, e.g. html 'br'",
        default="""br""",
        extra={"type": "Text"}
    )

@plugin
def settings_model():
    return MySettings

@hook
def before_cat_sends_message(message, cat):
    settings = cat.mad_hatter.get_plugin().load_settings()
    separator = "<" + settings["separator"] + ">"
    message["content"] = message["content"].replace("\n", separator)
    return message
