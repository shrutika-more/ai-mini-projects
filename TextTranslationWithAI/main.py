from deep_translator import GoogleTranslator


def translate_text(text, source, target):

    result = GoogleTranslator(
        source=source.lower(),
        target=target.lower()
    ).translate(text)

    return result