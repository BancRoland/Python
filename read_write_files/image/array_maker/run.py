from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
# sudo apt install python3-pillow

def format_for_c_array(array):
    result = "int array[60][10][3] = {\n"
    for i, row in enumerate(array):
        result += "  {\n"
        for j, col in enumerate(row):
            result += f"    {{{col[0]}, {col[1]}, {col[2]}}}"
            if j < len(row) - 1:
                result += ",\n"
            else:
                result += "\n"
        result += "  }"
        if i < len(array) - 1:
            result += ",\n"
        else:
            result += "\n"
    result += "};"
    return result

# Open an image file
image_path = 'test.png'
img = Image.open(image_path)

# Display basic information about the image
print(f"Image format: {img.format}")
print(f"Image size: {img.size}")
print(f"Image mode: {img.mode}")

# Optionally, display the image
# img.show()

img_array = np.array(img)

print(np.shape(img_array))      # (1366, 2048, 3)

img_arraySum=np.sum(img_array,axis=2)
# plt.imshow(img_array[:,:,1],cmap="gray")
plt.imshow(img_arraySum,cmap="gray")
plt.show()

# print(img)

formatted = format_for_c_array(img_array)

with open("led_data.c", "w") as f:
    f.write(formatted)

print("C array saved to led_data.c")