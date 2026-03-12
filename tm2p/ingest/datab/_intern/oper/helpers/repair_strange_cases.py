import pandas as pd  # type: ignore


def repair_strange_cases(text):
    if pd.isna(text):
        return text
    text = str(text)
    text = text.replace("_,_", "_")
    text = text.replace("_._", "_")
    text = text.replace(" :_", " : ")
    text = text.replace("_:_", " : ")
    text = text.replace("_S_", "_")
    text = text.replace("_http", " http")
    text = text.replace(" i . E . ", " i . e . ")
    text = text.replace(" . S . ", " . s . ")

    text = text.replace(" i.E. ", " i.e. ")
    text = text.replace(" E.g. ", " e.g. ")
    text = text.replace(" innwind.EU ", " innwind . eu ")
    text = text.replace(" you.s ", " you . s ")
    text = text.replace(" THE_F . E . c .", " the f . e . c .")

    text = text.replace(
        " . THE_CONTRIBUTIONS of THIS_PAPER are : ",
        " . the contributions of this paper are : ",
    )
    text = text.replace(
        ". THE_CONCLUSIONS can be summarized as follows :",
        ". the conclusions can be summarized as follows :",
    )

    return text
