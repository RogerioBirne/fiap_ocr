import pytesseract
from PIL import Image
from src import RESOURCES_PATH


def tesseract_example():
    img = Image.open(RESOURCES_PATH + '/Imagens/livro01.jpg')

    # plt.imshow(img)  # Show image
    # plt.waitforbuttonpress()  # wait for any press
    # plt.close()  # Close window

    osd = pytesseract.image_to_osd(img)   # Convert Image to osd with image infos
    print(osd)  # Print result


if __name__ == '__main__':
    tesseract_example()
