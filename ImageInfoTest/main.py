# from PIL import Image
# from PIL.PngImagePlugin import PngImageFile, PngInfo

# # im = Image.open('embeded.png')
# # metadata = PngInfo()
# # metadata.add_text("imageContent", 'shushushsu')
# # im.save("embeded3.png", format="PNG", pnginfo=metadata)

# im = Image.open('embeded3.png')
# EmbedInfoObj = im.text
# print('EmbedInfoObj', EmbedInfoObj)

import png

TEXT_CHUNK_FLAG = b'tEXt'


def generate_chunk_tuple(type_flag, content):
    return tuple([type_flag, content])


def generate_text_chunk_tuple(str_info):
    type_flag = TEXT_CHUNK_FLAG
    return generate_chunk_tuple(type_flag, bytes(str_info, 'utf-8'))


def insert_text_chunk(target, text, index=1):
    if index < 0:
        raise Exception('The index value {} less than 0!'.format(index))

    reader = png.Reader(filename=target)
    chunks = reader.chunks()
    chunk_list = list(chunks)
    print(chunk_list[0])
    print(chunk_list[1])
    print(chunk_list[2])
    chunk_item = generate_text_chunk_tuple(text)
    print('chunk_item', chunk_item)
    chunk_list.insert(index, chunk_item)

    with open(target, 'wb') as dst_file:
        png.write_chunks(dst_file, chunk_list)


def _insert_text_chunk_to_png_test():
    src = r'embeded3.png'
    insert_text_chunk(src, 'just for funny!')


if __name__ == '__main__':
    _insert_text_chunk_to_png_test()
