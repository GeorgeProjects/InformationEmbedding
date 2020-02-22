#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
import numpy as np 
from PIL import Image
import math


class Steganography(object):

    @staticmethod
    def __int_to_bin(rgb):
        """Convert an integer tuple to a binary (string) tuple.

        :param rgb: An integer tuple (e.g. (220, 110, 96))
        :return: A string tuple (e.g. ("00101010", "11101011", "00010110"))
        """
        # r, g, b, o = rgb
        return ('{0:08b}'.format(rgb[0]),
                '{0:08b}'.format(rgb[1]),
                '{0:08b}'.format(rgb[2]))

    @staticmethod
    def __bin_to_int(rgb):
        """Convert a binary (string) tuple to an integer tuple.
        :param rgb: A string tuple (e.g. ("00101010", "11101011", "00010110"))
        :return: Return an int tuple (e.g. (220, 110, 96))
        """
        r, g, b = rgb
        return (int(r, 2),
                int(g, 2),
                int(b, 2))

    @staticmethod
    def __merge_rgb(rgb1, rgb2):
        """Merge two RGB tuples.
        :param rgb1: A string tuple (e.g. ("00101010", "11101011", "00010110"))
        :param rgb2: Another string tuple
        (e.g. ("00101010", "11101011", "00010110"))
        :return: An integer tuple with the two RGB values merged.
        """
        r1, g1, b1 = rgb1
        r2, g2, b2 = rgb2
        rgb = (r1[:6] + r2[:1] + r2[:1],
               g1[:8],
               b1[:8])
        # print('rgb1', rgb1, 'rgb2', rgb2, 'rgb', rgb)
        return rgb

    @staticmethod
    def __merge_rgb_new(rgbH, rgbQ, pageNum):
        """Merge two RGB tuples.
        :param rgb1: A string tuple (e.g. ("00101010", "11101011", "00010110"))
        :param rgb2: Another string tuple
        (e.g. ("00101010", "11101011", "00010110"))
        :return: An integer tuple with the two RGB values merged.
        """
        rH, gH, bH = rgbH
        rQ, gQ, bQ = rgbQ
        colorSum = int(rQ, 2) + int(gQ, 2) + int(bQ, 2)
        if (colorSum != 0) and (colorSum != 765):
            print(colorSum)
        rgb = rgbH
        if pageNum == 0:
            rgb = (rH[:7] + rQ[:1],
                    gH[:8],
                    bH[:8])
        elif pageNum == 1:
            rgb = (rH[:6] + rQ[:1] + rH[7:8],
                    gH[:8],
                    bH[:8])
        elif pageNum == 2:
            rgb = (rH[:8],
                   gH[:7] + gQ[:1],
                   bH[:8])
        elif pageNum == 3:
            rgb = (rH[:8],
                   gH[:6] + gQ[:1] + gH[7:8],
                   bH[:8])
        elif pageNum == 4:
            rgb = (rH[:8],
                   gH[:8],
                   bH[:7] + bQ[:1])
        elif pageNum == 5:
            rgb = (rH[:8],
                   gH[:8],
                   bH[:6] + bQ[:1] + bH[7:8])
        return rgb

    # extract the qrcode image from the host image
    # @staticmethod
    # def parse_hidden_qrcode(hostImage, qrCodeCellNum, qrCodeCellMaxLen):
    #     hostImgWidth = hostImg.size[0]
    #     hostImgHeight = hostImg.size[1]
    #     hostImgMap = hostImg.load()
    #     qrCodeSideLength = qrCodeCellNum * qrCodeCellMaxLen
    #     qrCodeBitNum = qrCodeSideLength * qrCodeSideLength
    #     pageSum = 6
    #     hostBitNum = 0
    #     initQRCodeImg = PIL.Image.new(mode = "RGB", size = (qrCodeSideLength, qrCodeSideLength))
    #     initQRCodeImgMap = initQRCodeImg.load()
    #     for pageNum in range(pageSum):
    #         for i in range(hostImgWidth):
    #             for j in range(hostImgHeight):
    #                 # the count of the bits in the qr code
    #                 qrCodeBitPageNum = hostBitNum % qrCodeBitNum
    #                 qrCodeBitCol = qrCodeBitPageNum % qrCodeSideLength
    #                 qrCodeBitRow = qrCodeBitPageNum // qrCodeSideLength
    #                 rgbH = Steganography.__int_to_bin(hostImgMap[i, j])
    #                 modifyQRcodePixel(rgbH, pageNum, qrCodeBitCol, qrCodeBitRow, initQRCodeImgMap)
    #                 hostBitNum = hostBitNum + 1


    # modify the pixel value in the qrcode object of qrcode array
    @staticmethod
    def modifyQRcodePixel(rgbH, pageNum):
        rH, gH, bH = rgbH
        pixelBit = 1
        if pageNum == 0:
            pixelBit = rH[7:8]
        elif pageNum == 1:
            pixelBit = rH[6:7]
        elif pageNum == 2:
            pixelBit = gH[7:8]
        elif pageNum == 3:
            pixelBit = gH[6:7]
        elif pageNum == 4:
            pixelBit = bH[7:8]
        elif pageNum == 5:
            pixelBit = bH[6:7]
        # the final value of this pixel
        # print(pixelBit, 'pixelBit == 0', pixelBit == '0', 'pixelBit == 1', pixelBit == '1')
        if pixelBit == '1':
            return (255, 255, 255)
        elif pixelBit == '0':
            return (0, 0, 0)
         

    @staticmethod
    def parse_hidden_qrcode(hostImg, qrCodeCellNum, qrCodeCellMaxLen):
        hostImgWidth = hostImg.size[0]
        hostImgHeight = hostImg.size[1]

        hostImgMap = hostImg.load()
        qrCodeSideLength = qrCodeCellNum * qrCodeCellMaxLen
        print('parse qrcode length', qrCodeSideLength)
        qrCodeBitNum = qrCodeSideLength * qrCodeSideLength
        pageSum = 6
        hostBitNum = 0
        qrCodeNum = math.ceil((hostImgWidth * hostImgHeight * pageSum) / qrCodeBitNum)
        print('qrCodeNum', qrCodeNum)
        qrCodeImageArray = []
        qrCodeImageMapArray = []
        # initialize the qrcode array and qrcodeMap array
        for i in range(qrCodeNum):
            initQRCodeImg = Image.new(mode = "RGB", size = (qrCodeSideLength, qrCodeSideLength))
            initQRCodeImgMap = initQRCodeImg.load()
            qrCodeImageArray.append(initQRCodeImg)
            qrCodeImageMapArray.append(initQRCodeImgMap)
        # generate te qrcode image from the host image
        for pageNum in range(pageSum):
            for i in range(hostImgWidth):
                for j in range(hostImgHeight):
                    # the count of the bits in the qr code
                    qrCodeBitIndex = hostBitNum % qrCodeBitNum
                    qrCodeIndex = math.floor(hostBitNum / qrCodeBitNum)
                    qrCodeImageMap = qrCodeImageMapArray[qrCodeIndex]
                    qrCodeBitCol = qrCodeBitIndex % qrCodeSideLength
                    qrCodeBitRow = math.floor(qrCodeBitIndex / qrCodeSideLength)
                    rgbH = Steganography.__int_to_bin(hostImgMap[i, j])
                    qrCodeImageMap[qrCodeBitCol, qrCodeBitRow] = Steganography.modifyQRcodePixel(rgbH, pageNum)
                    hostBitNum = hostBitNum + 1
        return qrCodeImageArray
    
    @staticmethod
    def merge2(hostImageMapPixel, qrcodeImgBit, channelIndex):
        print('hostImageMapPixel', hostImageMapPixel, 'qrcodeImgBit', qrcodeImgBit, 'channelIndex', channelIndex)
        
    # merge the qrcode image into the host image
    @staticmethod
    def merge_new (hostImg, qrcodeImg, pageRowNum, pageColNum, pageNum):
        qrcodeImgWidth = qrcodeImg.size[0]
        qrcodeImgHeight = qrcodeImg.size[1]
        hostImgWidth = hostImg.size[0]
        hostImgHeight = hostImg.size[1]
        hostImgMap = hostImg.load()
        qrcodeImgMap = qrcodeImg.load()
        for i in range(qrcodeImgWidth * qrcodeImgHeight):
            hostImgPixelCol = (i + pageColNum) % hostImgWidth
            hostImgPixelRow = (i + pageColNum) // hostImgWidth + pageRowNum
            currentPageNum = pageNum
            if hostImgPixelRow >= hostImgHeight:
                hostImgPixelRow = hostImgPixelRow % hostImgHeight
                currentPageNum = pageNum + 1
            qrcodeImgPixelCol = i % qrcodeImgWidth
            qrcodeImgPixelRow = i // qrcodeImgWidth
            rgbH = Steganography.__int_to_bin(hostImgMap[hostImgPixelCol, hostImgPixelRow])
            rgbQ = Steganography.__int_to_bin((0, 0, 0))
            if isinstance(qrcodeImgMap[qrcodeImgPixelCol, qrcodeImgPixelRow], int):
                if qrcodeImgMap[qrcodeImgPixelCol, qrcodeImgPixelRow] == 255:
                    rgbValue = (255, 255, 255)
                    rgbQ = Steganography.__int_to_bin(rgbValue)
                else:
                    rgbValue = (0, 0, 0)
                    rgbQ = Steganography.__int_to_bin(rgbValue)
            else:
                rgbQ = Steganography.__int_to_bin(qrcodeImgMap[qrcodeImgPixelCol, qrcodeImgPixelRow])
                # Merge the two pixels and convert it to a integer tuple
            rgbH_new = Steganography.__merge_rgb_new(rgbH, rgbQ, currentPageNum)
            hostImgMap[hostImgPixelCol, hostImgPixelRow] = Steganography.__bin_to_int(rgbH_new)
        return hostImg

    @staticmethod
    def merge(img1, img2, startPos, max_qr_image_length):
        """Merge two images. The second one will be merged into the first one.

        :param img1: First image
        :param img2: Second image
        :return: A new merged image.
        """

        # Check the images dimensions
        if img2.size[0] > img1.size[0] or img2.size[1] > img1.size[1]:
            raise ValueError('Image 2 should not be larger than Image 1!')

        # Get the pixel map of the two images
        pixel_map1 = img1.load()
        pixel_map2 = img2.load()
        # print('startPos', startPos, 'max_qr_image_length', max_qr_image_length)
        for i in range(startPos[0], (startPos[0] + max_qr_image_length)):
            for j in range(startPos[1], (startPos[1] + max_qr_image_length)):
                rgb1 = Steganography.__int_to_bin(pixel_map1[i, j])
                # Use a black pixel as default
                rgb2 = Steganography.__int_to_bin((0, 0, 0))
                qrCode_i = i - startPos[0]
                qrCode_j = j - startPos[1]
                # Check if the pixel map position is valid for the second image
                if qrCode_i < img2.size[0] and qrCode_j < img2.size[1]:
                    # print('pixel_map2', pixel_map2[qrCode_i, qrCode_j])
                    # if i <= 100 and j <= 100:
                    if isinstance(pixel_map2[qrCode_i, qrCode_j], int):
                        if pixel_map2[qrCode_i, qrCode_j] == 255:
                            rgbValue = (255, 255, 255)
                            rgb2 = Steganography.__int_to_bin(rgbValue)
                        else:
                            rgbValue = (0, 0, 0)
                            rgb2 = Steganography.__int_to_bin(rgbValue)
                    else:
                        rgb2 = Steganography.__int_to_bin(pixel_map2[qrCode_i, qrCode_j])
                # Merge the two pixels and convert it to a integer tuple
                rgb = Steganography.__merge_rgb(rgb1, rgb2)
                pixel_map1[i, j] = Steganography.__bin_to_int(rgb)

        return img1

    @staticmethod
    def unmerge(img):
        """Unmerge an image.

        :param img: The input image.
        :return: The unmerged/extracted image.
        """

        # Load the pixel map
        pixel_map = img.load()
        # Create the new image and load the pixel map
        new_image = Image.new(img.mode, img.size)
        pixels_new = new_image.load()

        # Tuple used to store the image original size
        original_size = img.size

        for i in range(img.size[0]):
            for j in range(img.size[1]):
                # Get the RGB (as a string tuple) from the current pixel
                r, g, b = Steganography.__int_to_bin(pixel_map[i, j])
                # u_rbg = Steganography.__int_to_bin(pixel_map[i, j])
                intR = int(r[4:] + '0000', 2)
                intG = int(g[4:] + '0000', 2)
                intB = int(b[4:] + '0000', 2)
                avgRGB = (intR + intG + intB) / 3
                maxRGB = max(intR, intG, intB)
                # print (maxRGB)
                rgb = ('00000000', '00000000', '00000000')
                if maxRGB <= 180:
                    rgb = ('11111111', '11111111', '11111111')
                # Extract the last 4 bits (corresponding to the hidden image)
                # Concatenate 4 zero bits because we are working with 8 bit
                # rgb = (r[4:] + '0000',
                #        g[4:] + '0000',
                #        b[4:] + '0000')

                # Convert it to an integer tuple
                pixels_new[i, j] = Steganography.__bin_to_int(rgb)

                # If this is a 'valid' position, store it
                # as the last valid position
                if pixels_new[i, j] != (0, 0, 0):
                    original_size = (i + 1, j + 1)

        # Crop the image based on the 'valid' pixels
        new_image = new_image.crop((0, 0, original_size[0], original_size[1]))

        return new_image


@click.group()
def cli():
    pass


@cli.command()
@click.option('--img1', required=True, type=str, help='Image that will hide another image')
@click.option('--img2', required=True, type=str, help='Image that will be hidden')
@click.option('--output', required=True, type=str, help='Output image')
def merge(img1, img2, output):
    merged_image = Steganography.merge(Image.open(img1), Image.open(img2))
    merged_image.save(output)


@cli.command()
@click.option('--img', required=True, type=str, help='Image that will be hidden')
@click.option('--output', required=True, type=str, help='Output image')
def unmerge(img, output):
    unmerged_image = Steganography.unmerge(Image.open(img))
    unmerged_image.save(output)


if __name__ == '__main__':
    cli()
