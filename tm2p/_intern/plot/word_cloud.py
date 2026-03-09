import numpy as np
from wordcloud import WordCloud as WordCloudExternal  # type: ignore


def word_cloud(params, dataframe):

    width = params.plot_width
    height = params.plot_height

    mask_size = min(width, height)
    center = mask_size // 2
    radius = int(center * 0.87)  # 87% of center to leave margin

    x_mask, y_mask = np.ogrid[:mask_size, :mask_size]
    mask = (x_mask - center) ** 2 + (y_mask - center) ** 2 > radius**2
    mask = 255 * mask.astype(int)

    wordcloud = WordCloudExternal(
        background_color="white",
        repeat=True,
        mask=mask,
        width=width,
        height=height,
    )

    text = dict(
        zip(
            dataframe.index,
            dataframe[params.items_order_by.value],
        )
    )
    wordcloud.generate_from_frequencies(text)
    wordcloud.recolor(color_func=lambda word, **kwargs: "black")

    fig = wordcloud.to_image()

    return fig
