import cv2
import pydicom as dicom
import numpy as np
import os

def BrightnessContrast(brightness=0):

    global filename
    # getTrackbarPos returns the current
    # position of the specified trackbar.
    dst = "/home/abhinav/gsoc/ct_image_scanning/lab_tech/dst/"
    brightness = cv2.getTrackbarPos('Brightness',
                                    'DICOM Image')

    contrast = cv2.getTrackbarPos('Contrast',
                                  'DICOM Image')

    effect = controller(original, brightness,
                        contrast)

    # The function imshow displays an image
    # in the specified window
    cv2.imshow('Effect', effect)
    cv2.imwrite(os.path.join(dst, str(filename)), effect)


def controller(img, brightness=255,
               contrast=127):
    brightness = int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255))
    contrast = int((contrast - 0) * (127 - (-127)) / (254 - 0) + (-127))
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            max = 255
        else:
            shadow = 0
            max = 255 + brightness
        al_pha = (max - shadow) / 255
        ga_mma = shadow
    
        cal = cv2.addWeighted(img, al_pha,
                              img, 0, ga_mma)

    else:
        cal = img

    if contrast != 0:
        Alpha = float(131 * (contrast + 127)) / (127 * (131 - contrast))
        Gamma = 127 * (1 - Alpha)

        cal = cv2.addWeighted(cal, Alpha,
                              cal, 0, Gamma)

    cv2.putText(cal, 'B:{},C:{}'.format(brightness,
                                        contrast), (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    return cal


if __name__ == '__main__':
    # The function imread loads an image
    # from the specified file and returns it.
    UPLOAD_FOLDER = "/home/abhinav/gsoc/ct_image_scanning/lab_tech/src/"
    PNG = False
    file_path = "/home/abhinav/gsoc/ct_image_scanning/lab_tech/img.dcm"
    filename = "img.dcm"
    
    # Reading DICOM
    ds = dicom.dcmread(file_path)
    test90 = ds.pixel_array
    test90 = ds.pixel_array.astype(float)
    threshold = 500
    test90 = (np.maximum(test90, 0) / (np.amax(test90) + threshold)) * 255.0
    if PNG == False:
        filename = filename.replace('.dcm', '.jpg')
    else:
        filename = filename.replace('.dcm', '.png')
    cv2.imwrite(os.path.join(UPLOAD_FOLDER, filename), test90)
    original = cv2.imread(os.path.join(UPLOAD_FOLDER, filename))

    cv2.namedWindow('DICOM Image')

    cv2.imshow('DICOM Image', original)

    cv2.createTrackbar('Brightness',
                    'DICOM Image', 255, 2 * 255,
                    BrightnessContrast)

    cv2.createTrackbar('Contrast', 'DICOM Image',
                    127, 2 * 127,
                    BrightnessContrast)

    while True:
        k=cv2.waitKey(1) & 0xFF
        if k == ord('s'):
            BrightnessContrast(0)
            print("Saved image")
        if k==ord('q'):
            break
    cv2.destroyAllWindows()

# The function waitKey waits for
# a key event infinitely or for delay
# milliseconds, when it is positive.
