import cv2 as cv2
import numpy as np

# This function will get click pixel coordinate that source image will be pasted to destination image

def get_paste_position(event, x, y, flags, paste_coordinate_list):
    cv2.imshow('collect coordinate', img_dest_copy)
    if event == cv2.EVENT_LBUTTONUP:
    
    # Draw circle right in click position
    cv2.circle(img_dest_copy, (x, y), 2, (0, 0, 255), -1)
    
    # Append new clicked coordinate to paste_coordinate_list
    paste_coordinate_list.append([x, y])
if __name__ == '__main__':
    
    # Read source image
    img_src = cv2.imread('woman-1807533_960_720.webp', cv2.IMREAD_COLOR)
    
    # cv2.imwrite('source_image.jpg', img_src)
    h, w, c = img_src.shape
    
    # Get source image parameter: [[left,top], [left,bottom], [right, top], [right, bottom]]
    img_src_coordinate = np.array([[0,0],[0,h],[w,0],[w,h]])
    
    # Read destination image
    img_dest = cv2.imread('billboard-g7005ff0f9_1920.jpg', cv2.IMREAD_COLOR)
    
    # copy destination image for get_paste_position (Just avoid destination image will be draw)
    img_dest_copy = img_dest.copy()#np.tile(img_dest, 1)
    
    # paste_coordinate in destination image
    paste_coordinate = []
    cv2.namedWindow('collect coordinate')
    cv2.setMouseCallback('collect coordinate', get_paste_position, paste_coordinate)
    
    while True:
        cv2.waitKey(1)
        if len(paste_coordinate) == 4:
            break
    paste_coordinate = np.array(paste_coordinate)
    
    # Get perspective matrix
    matrix, _ = cv2.findHomography(img_src_coordinate, paste_coordinate, 0)
    print(f'matrix: {matrix}')
    perspective_img = cv2.warpPerspective(img_src, matrix, (img_dest.shape[1], img_dest.shape[0]))
    cv2.imshow('img', perspective_img)
    cv2.copyTo(src=perspective_img, mask=np.tile(perspective_img, 1), dst=img_dest)
    cv2.imshow('result', img_dest)
    cv2.waitKey()
    cv2.destroyAllWindows()