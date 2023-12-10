import termcolor

def perlin_ascii(width, height, scale):
    from perlin_noise import PerlinNoise
    from random import randint
    noise1 = PerlinNoise(seed=randint(0,1000),octaves=3)
    noise2 = PerlinNoise(seed=randint(0,1000),octaves=6)
    noise3 = PerlinNoise(seed=randint(0,1000),octaves=12)
    noise4 = PerlinNoise(seed=randint(0,1000),octaves=24)

    def convert_brightness(vals, a, b, ascii_symbols, colors_list):
        def clamp(num, min_value, max_value):
            num = max(min(num, max_value), min_value)
            return num
        # Determine the range of values we need to convert
        val_range = b - a

        # Convert each value in the list to a brightness level
        brightness_levels = []
        for val in vals:
            # Map the value to a float in the range [0, 1]
            normalized_val = (val - a) / val_range

            # Calculate the index of the ascii symbol to use
            ascii_index = int(normalized_val * (len(ascii_symbols) - 1))
            ascii_index = clamp(ascii_index, 0, len(ascii_symbols)-1)

            color_index = int(normalized_val * (len(colors_list) - 1))
            color_index = clamp(color_index, 0, len(colors_list)-1)

            # Add the corresponding ascii symbol to the list
            brightness_levels.append(termcolor.colored(ascii_symbols[ascii_index], colors_list[color_index]))
        return brightness_levels
    ascii_symbols = [' ', '.', ',', '-', '~', '=', '+', '*', '#', '$']
    colors = ['black', 'dark_grey', 'grey', 'light_grey', 'white', 
            'red', 'green', 'blue', 'magenta', 'cyan', 'yellow', 
            'light_red', 'light_green', 'light_blue', 'light_magenta', 
            'light_cyan', 'light_yellow']

    h = height
    w = width
    pic = ''
    for i in range(w):
        row = []
        for j in range(h):
            noise_val = noise1([i/(w*scale), j/(h*scale)])
            noise_val += 0.5 * noise2([i/(w*scale), j/(h*scale)])
            noise_val += 0.25 * noise3([i/(w*scale), j/(h*scale)])
            noise_val += 0.125 * noise4([i/(w*scale), j/(h*scale)])
            row.append(noise_val)
        as_text = convert_brightness(row, min(row), max(row), ascii_symbols, colors)
        pic += ''.join(as_text) + '\n'
    return pic.rstrip('\n')