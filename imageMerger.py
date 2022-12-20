from PIL import Image

def measureImage(image):
    width, height = image.size #measure size
    print(f"Background image is: Width:{width} and height:{height}")
    # measure differences between template and background
    h1 = (1000-height)*1/3 #top
    h2 = (1000-height)*2/3 #bottom
    h = [h1, h2]
    # creating a image object (new image object) with
    # RGB mode and size 200x200
    for i in h:
        print("Creating img with height", int(i))
        im = Image.new(mode="RGB", size=(1000, int(i)), color="white")

    # This method will show image in any image viewer
        total_image = imagesConcatenate(image, im, int(i))
        print("Total image ready")
        # total_image.show()
        return total_image

def imagesConcatenate(mainIm, addIm, heghtSize):
    # opening up of images
    # creating a new image and pasting the
    # images
    whole_image = Image.new("RGB", (1000, 1000), "white")
    # pasting the first image (image_name,
    # (position))
    whole_image.paste(addIm, (0, 0))
    # pasting the second image (image_name,
    # (position))
    whole_image.paste(mainIm, (0, heghtSize))
    # whole_image.save("whole_image.png")
    return whole_image

def changeImageSize(maxWidth, image):
    widthRatio = maxWidth / image.size[0]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(widthRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

def merge_items(background, overlay, directory):
    background = background.convert("RGBA")
    overlay = overlay.convert("RGBA")
    new_img = Image.alpha_composite(background, overlay)
    width, height = new_img.size #measure size
    print(f"Final picture is: Width:{width} and height:{height}")
    new_img.save(f"{directory}/final_pic.png","PNG")
    # new_img.show()
    return new_img


def main(file, directory):
    background = Image.open(file)
    overlay = Image.open("./overlay.png")
    bg = changeImageSize(1000, background)  # changing size proportianlly woth new width
    new_bg = measureImage(bg)  # creating additional images
    final_image = merge_items(new_bg, overlay, directory)


if __name__ == "__main__":
    main()