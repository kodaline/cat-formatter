import re
from typing import Literal
from cat.mad_hatter.decorators import tool, hook, plugin
from pydantic import BaseModel, Field
from cat.log import log

class MySettings(BaseModel):
    br: bool = Field(
        title="br tag",
        description="Activates the br tag line separator",
        default=True,
    )
    hr: bool = Field(
    default=False,
    description="Activates the hr tag line separator",
    title="hr tag",
    )
    if hr:
        style: str = Field(
        default="solid",
        description="hr tag separator style (applies only if hr is active). Possible values: solid, dotted, rounded, dashed",
        title="hr tag style",
    )

@plugin
def settings_model():
    return MySettings

@hook
def before_cat_sends_message(message, cat):
    settings = cat.mad_hatter.get_plugin().load_settings()
    br_active = settings["br"]
    hr_active = settings["hr"]
    tags = []
    style = ""
    if br_active and hr_active:
        tags.append("<br><br>")
        style = hr_styles(settings["style"])
        tags.append("<hr style=\"" + style + "\">")
        tags.append("<br>")
        separator = "".join(tags)
        text = re.split(r'\n+', message["content"], flags=re.M)
        log.error(text)
        message["content"] = separator.join(filter(lambda e: e!="", text))
        return message
    if br_active:
        tags.append("<br><br>")
    if hr_active:
        style = hr_styles(settings["style"])
        tags.append("<hr style=\"" + style + "\">")
    separator = "".join(tags)
    if separator:
        text = re.split(r'\n+', message["content"], flags=re.M)
        log.error(text)
        message["content"] = separator.join(text)
    return message

def hr_styles(style):
    # Dashed border
    if style == "dashed":
        return "border-top: 2px dashed #bbb;"
        # Dotted border
    elif style == "dotted":
        return "border-top: 2px dotted #bbb;"
        # Solid border
    elif style == "solid":
        return "border-top: 2px solid #bbb;"
    elif style == "rounded":
        # Rounded border
        return "border-top: 2px solid #bbb; border-radius: 4px;"
    else:
        return "border-top: 2px solid #bbb;"