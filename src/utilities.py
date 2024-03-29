from math import exp


def smoothing_function(x: float, x_min: float, x_max: float, y_min: float, y_max: float) -> float:
    """
    Uses a sigmoid function to smooth based on the argument bounds
    https://en.wikipedia.org/wiki/Sigmoid_function
    :param x: independent variable
    :param x_min: minimum value of x
    :param x_max: maximum value of x
    :param y_min: minimum value of y
    :param y_max: maximum value of y
    :return: smoothed float between y_min and y_max
    """

    if x < x_min:
        return y_min
    elif x > x_max:
        return y_max
    else:
        x_normalized = (x - x_min) / (x_max - x_min)

    # scales x = [0, 1] to [-4, 4]
    x_sig = 8.0 * x_normalized + -4.0

    # compute sigmoid
    # y_sig = 1 / (1 + exp(-x_sig))

    # tuned parameters
    # Parameters tuned ensure the normalized sigmoid satisfies (x, y) = (-4, 0) and (4, 1)
    # when x = -4 and 4, the derivative of the sigmoid function is < 0.01.
    # This ensures that the sigmoid transition at those points is very nearly flat, but begins to
    # smoothly transition immediately.
    a = 1.0373140383507
    b = 0.0186560820737
    y_sig = a / (1 + exp(-x_sig)) - b

    return (y_max - y_min) * y_sig + y_min
