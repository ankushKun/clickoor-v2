import cv2


def make_alpha(path: str):
    # Read the PNG image
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)

    # Get the alpha channel
    alpha_channel = img[:, :, 3]

    # Save the alpha channel as a grayscale image
    f = path.split(".")
    cv2.imwrite("".join(f[:-1]) + ".mask.png", alpha_channel)


make_alpha("assets/shutter.png")
