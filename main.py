from PIL import ImageDraw, ImageFont, Image
from pathlib import Path
import progressbar
import argparse

import config

class ImageGenerator():
    def __init__(self, output_path, default_format = '.png'):
        print('[INFO] ImageGenerator class initialization')

        self.Alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
        self.alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        self.symbols = '.,\/#!$%^&*;:{}=-_`~()[]?"\''
        self.numbers = '0123456789'
        self.badSymbols = {
            '>': 'more',
            '<': 'less',
            ':': 'dots',
            '"': 'dquote',
            '/': 'fslash',
            '\\': 'bslash',
            '|': 'vslash',
            '?': 'quest',
            '*': 'star'
        }

        self.outputPath = output_path
        self.defaultFormat = default_format if default_format[0] == '.' else '.' + default_format

    def generate(self, img_size, font_path, offsets = [(0, 0)], max_angle = 0, angle_step = 1, font_size = 10, img_mode = '1'):
        font = None
        if Path(font_path).suffix.lower() == '.ttf':
            print('[INFO] Using truetype font')
            font = ImageFont.truetype(font_path, size = font_size)
        else:
            print('[INFO] Using not truetype font')
            font = ImageFont.load(font_path)
            
        fontName =  '_'.join(font.getname()) + '-' + f'{img_size[0]}x{img_size[1]}'
        
        # Create necessary folders
        Path(self.outputPath).joinpath(fontName).mkdir(parents = True, exist_ok = True)

        allSymbols = self.__get_all_symbols()

        #-------------
        widgets = ['[GENERATING] ', progressbar.Bar(), ' =', progressbar.ETA(), '= ']
        pbar = progressbar.ProgressBar(max_value = len(allSymbols), widgets = widgets)
        #-------------

        for idx, c in enumerate(allSymbols):
            baseImgName = fontName + '-' + (self.badSymbols[c] if c in self.badSymbols else c) + (c if c in self.Alphabet else '')
            tSize = font.getsize(c)
            tOffset = font.getoffset(c)

            for off in offsets:
                tCenter = (
                    img_size[0] / 2 - (tSize[0] - tOffset[0]) / 2 + off[0],
                    img_size[1] / 2 - (tSize[1] + tOffset[1]) / 2 + off[1]
                )

                for angle in range(0, max_angle + 1, angle_step):
                    self.__save_image(fontName, img_size, baseImgName, img_mode, c, font, tCenter, off, angle)
                for angle in range(0, -max_angle - 1, -angle_step):
                    self.__save_image(fontName, img_size, baseImgName, img_mode, c, font, tCenter, off, angle)

            pbar.update(idx)

    # Saving image function
    def __save_image(self, font_name, img_size, base_img_name, img_mode, text, text_font, text_center, offset, img_angle):
        imgName = base_img_name + f'-off{offset[0]}_{offset[1]}' + f'-a{img_angle}' + self.defaultFormat
        imgPath = Path(self.outputPath).joinpath(font_name, imgName)
        with Image.new(img_mode, img_size) as img:
            dr = ImageDraw.Draw(img)
            dr.text(text_center, text, fill = '#fff', font = text_font)
            img = img.rotate(img_angle)
            img.save(imgPath)

    # Get all symbols function
    def __get_all_symbols(self):
        return self.Alphabet + self.alphabet + self.symbols + self.numbers

if __name__ == '__main__':
    imGen = ImageGenerator(config.OUTPUT_FOLDER_PATH, default_format = config.IMAGE_FORMAT)
    imGen.generate(config.IMAGE_SIZE, config.INPUT_FONT, font_size = config.FONT_SIZE, offsets = config.OFFSETS_VALUES, max_angle = config.MAX_ANGLE, angle_step = config.ANGLE_STEP)