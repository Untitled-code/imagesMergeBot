from PIL import Image, ImageDraw, ImageFont
import textwrap


def draw_multiple_line_text(image, text, font, text_color, text_start_height):
    '''
    From unutbu on [python PIL draw multiline text on image](https://stackoverflow.com/a/7698300/395857)
    '''
    draw = ImageDraw.Draw(image)
    # image_width, image_height = image.size #alignment center side
    y_text = text_start_height
    lines = textwrap.wrap(text, width=36)
    for line in lines:
        line_width, line_height = font.getsize(line)
        # draw.text(((image_width - line_width) / 2, y_text), #alignment center side
        draw.text((100, y_text), #alignment left side
                  line, font=font, fill=text_color)
        y_text += line_height + 5

def main(text1, text2, directory):
    '''
    Testing draw_multiple_line_text
    '''
    #image_width
    image = Image.open(f"./{directory}/final_pic.png")
    fontsize = 44  # starting font size
    font = ImageFont.truetype("arialbd.ttf", fontsize, encoding='utf-8')
    font2 = ImageFont.truetype("arialbd.ttf", 36, encoding='utf-8')
    # # text1 = "Росіяни навмисне підірвали водопровід до Миколаєва, місто шостий місяць без питної води"
    # # text2 = "Прифронтовий Миколаїв вже шість місяців не має питної води. " \
    #         "Російські окупанти у квітні 2022 року підірвали водопровід, яким у місто надходила чиста вода."

    text_color = "yellow"
    text_start_height = 30
    draw_multiple_line_text(image, text1, font, text_color, text_start_height)
    draw_multiple_line_text(image, text2, font2, "white", 650)
    image.show()
    image.save(f'{directory}/pic_text.png')

if __name__ == "__main__":
    main()
    #cProfile.run('main()') # if you want to do some profiling