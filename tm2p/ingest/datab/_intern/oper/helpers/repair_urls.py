import re


def repair_urls(text, matches):
    if len(matches) == 0:
        return text
    for match in matches:
        regex = re.compile(re.escape(match), re.IGNORECASE)
        text = regex.sub(lambda z: z.group().lower(), text)
    return text
