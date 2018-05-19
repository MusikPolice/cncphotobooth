import cv2
import subprocess

# path to input file
# TODO: use the pi's camera instead
INPUT_FILENAME = '/home/jfritz/Downloads/redhead.jpg'
TEMP_FILENAME = '/home/jfritz/Downloads/redhead'

# these three values control the amount of detail in the final line drawing
BLUR_AMOUNT = 5
CANNY_THRESHOLD = 40

# these control final size of the image as drawn by the CNC
SVG_MAX_HEIGHT_INCHES = 7
SVG_MAX_WIDTH_INCHES = 9
MARGIN_INCHES = 0.25

# read the input image
greyscale = cv2.imread(INPUT_FILENAME, 0)
inputWidth = greyscale.shape[1]
inputHeight = greyscale.shape[0]
print 'Input image width=' + str(inputWidth) + ', height=' + str(inputHeight)

# edge detection
blur = cv2.medianBlur(greyscale, BLUR_AMOUNT)
edges = cv2.Canny(blur, CANNY_THRESHOLD, CANNY_THRESHOLD*2, L2gradient=True)
cv2.imwrite(TEMP_FILENAME + '.bmp', edges)

# use potrace to trace the bitmap into an svg, respecting aspect ratio and margins
# TODO: apprenticemarks logo
svgHeight = SVG_MAX_HEIGHT_INCHES - (2*MARGIN_INCHES)
aspectRatio = float(inputWidth)/float(inputHeight)
svgWidth = svgHeight * aspectRatio
if svgWidth > SVG_MAX_WIDTH_INCHES:
    print 'Using width as max dimension'
    svgWidth = SVG_MAX_WIDTH_INCHES - (2*MARGIN_INCHES)
    aspectRatio = float(inputHeight)/float(inputWidth)
    svgHeight = svgWidth * aspectRatio
else:
    print 'Using height as max dimension'
    
print 'Output aspect ratio is ' + str(aspectRatio)
print 'SVG width=' + str(svgWidth + (2*MARGIN_INCHES)) + 'in, SVG height=' + str(svgHeight + (2*MARGIN_INCHES)) + 'in'
subprocess.check_call('potrace --output ' + TEMP_FILENAME + '.svg --svg --width ' + str(svgWidth) + 'in --height ' + str(svgHeight) + 'in --margin ' + str(MARGIN_INCHES) + 'in --invert ' + TEMP_FILENAME + '.bmp', shell=True)

# TODO: turn the svg into gcode

# cleanup once window is closed
cv2.waitKey()
cv2.destroyAllWindows()