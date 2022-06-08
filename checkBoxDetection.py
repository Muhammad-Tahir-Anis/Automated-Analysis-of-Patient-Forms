from operator import itemgetter
import pandas as pd
import numpy as np
import cv2


def select_image(image_path):
    # img_path = image_path
    image = cv2.imread(image_path)
    return image


def convert_image_to_binary(image):
    gray_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    th1, img_bin = cv2.threshold(gray_scale, 150, 225, cv2.THRESH_BINARY)
    img_bin = ~img_bin
    return img_bin


def image_size(image):
    height, width, channels = image.shape
    return height, width


def find_checkboxes(img_bin, line_min_width=15):
    kernel_h = np.ones((1, line_min_width), np.uint8)
    kernel_v = np.ones((line_min_width, 1), np.uint8)
    img_bin_h = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernel_h)
    img_bin_v = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernel_v)
    img_bin_final = img_bin_h | img_bin_v
    final_kernel = np.ones((3, 3), np.uint8)
    img_bin_final = cv2.dilate(img_bin_final, final_kernel, iterations=1)
    retval, labels, stats, centroids = cv2.connectedComponentsWithStats(~img_bin_final, connectivity=8,
                                                                        ltype=cv2.CV_32S)
    for x, y, w, h, area in stats:
        cv2.rectangle(img_bin, (x, y), (x + w, y + h), (0, 255, 0), 2)
    checkboxes = []
    print(stats)
    for stat in stats:
        if 25 > stat[2] > 5 and 25 > stat[3] > 5:
            checkboxes.append(stat)
    return checkboxes


def first_checkbox_location(checkboxes):
    x_axis = []
    y_axis = []
    for checkbox in checkboxes:
        x_axis.append(checkbox[0])
        y_axis.append(checkbox[1])
    start_x_axis = min(x_axis)
    print(start_x_axis)
    start_y_axis = min(y_axis)
    print(start_y_axis)
    end_x_axis = max(x_axis)
    end_y_axis = max(y_axis)
    return start_x_axis, start_y_axis, end_x_axis, end_y_axis


def arrange_checkboxes(checkboxes):
    arranged_checkboxes = []
    checkbox_row = []
    y = checkboxes[0][1]
    for checkbox in checkboxes:
        if y - 10 < checkbox[1] < y + 10:
            checkbox_row.append(checkbox)
        else:
            y = checkbox[1]
            arranged_checkboxes.append(checkbox_row)
            checkbox_row = [checkbox]
    arranged_checkboxes.append(checkbox_row)
    checkbox_row = []

    sort_checkboxes = []
    for checkboxes in arranged_checkboxes:
        checkboxes = sorted(checkboxes, key=itemgetter(0))
        sort_checkboxes.append(checkboxes)
    print(sort_checkboxes)
    return arranged_checkboxes, sort_checkboxes


def checkbox_status(img_bin, arranged_checkboxes):
    pixels = []
    pixel = []
    for checkboxes in arranged_checkboxes:
        for checkbox in checkboxes:
            crop_img = img_bin[checkbox[1]:checkbox[1] + checkbox[2], checkbox[0]:checkbox[0] + checkbox[3]]
            thresh1 = cv2.threshold(crop_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

            pixel.append(cv2.countNonZero(thresh1))
        pixels.append(pixel)
        pixel = []
    print(pixels)
    return pixels


def marked_checkboxes(pixels_array):
    rows_status = []
    for pixels in pixels_array:
        counter = 0
        index = ''
        row_status = []
        for pixel in pixels:
            if pixel > 60:
                index = pixels.index(pixel)+1
                counter += 1
        if counter < 1 or counter > 1:
            index = 0
        row = pixels_array.index(pixels)
        row_status.append(row)
        row_status.append(index)
        rows_status.append(row_status)
        # print(index1,index)
    return rows_status



def run_analysis(image_path):
    image = select_image(image_path)
    cv2.imshow('image', image)
    cv2.waitKey(0)
    image_height, image_width = image_size(image)
    img_bin = convert_image_to_binary(image)
    cv2.imshow('image', img_bin)
    cv2.waitKey(0)
    checkboxes = find_checkboxes(img_bin)
    print(checkboxes)
    arranged_checkboxes, sort_checkboxes = arrange_checkboxes(checkboxes)
    pixels = checkbox_status(img_bin, sort_checkboxes)
    cv2.imshow('image', img_bin)
    cv2.waitKey(0)

    rows_status = marked_checkboxes(pixels)
    answers = []
    for status in rows_status:
        answers.append(status[1])
    max_value = np.max(answers)
    length_answers=len(answers)
    for value in range(0,max_value+1):
        print(f"Percentage of  {value}  is  {answers.count(value) / length_answers * 100}")
        answers.append(f"Percentage of  {value}  is  {answers.count(value) / length_answers * 100}")
    df = pd.DataFrame(answers).T
    df.to_csv("F:/Text Images/Data.csv", mode='a',index=False, header=False)
    for row_status in rows_status:
        print(row_status[1])
    img = cv2.resize(image, (750, 750))
    cv2.imshow('image', img)
    cv2.waitKey(0)

# run_analysis("C:/Users/hp/Downloads/TESTING DATA/testing/page-0.png")