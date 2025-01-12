from PIL import Image, ImageDraw
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def count_and_mark_dominant_red_pixels(image_path, output_path, log_path):
    """
    Counts the number of pixels where the red color is dominant in the given image,
    logs the details, and marks the top 3 most dominant red pixels with rectangles in the output image.

    Args:
        image_path (str): The path to the image file.
        output_path (str): The path to save the output image.
        log_path (str): The path to save the log file.

    Returns:
        int: The number of pixels with dominant red color.
    """
    try:
        with Image.open(image_path) as img:
            img = img.convert("RGB")
            width, height = img.size
            pixels = img.load()
            red_dominant_count = 0
            log_entries = []
            draw = ImageDraw.Draw(img)
            top_red_pixels = []

            for x in range(width):
                for y in range(height):
                    r, g, b = pixels[x, y]
                    total = r + g + b
                    if total > 0 and r / total >= 0.51:
                        red_dominant_count += 1
                        log_entries.append(f"{red_dominant_count} - [{r},{g},{b}] - {x},{y}")
                        top_red_pixels.append((r, x, y, red_dominant_count))
                        top_red_pixels = sorted(top_red_pixels, reverse=True)[:3]

            marked_rectangles = mark_top_red_pixels(draw, top_red_pixels)

            img.save(output_path)
            save_log(log_path, log_entries)

            return red_dominant_count

    except FileNotFoundError:
        logging.error(f"The file {image_path} was not found.")
        return None
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None

def mark_top_red_pixels(draw, top_red_pixels):
    def rectangles_overlap(rect1, rect2):
        return not (rect1[2] < rect2[0] or rect1[0] > rect2[2] or rect1[3] < rect2[1] or rect1[1] > rect2[3])

    marked_rectangles = []

    for r, x, y, pixel_number in top_red_pixels:
        new_rect = [x-5, y-5, x+5, y+5]
        if all(not rectangles_overlap(new_rect, rect) for rect in marked_rectangles):
            draw.rectangle(new_rect, outline="red")
            draw.text((x+15, y+15), str(pixel_number), fill="red")
            marked_rectangles.append(new_rect)
    
    return marked_rectangles

def save_log(log_path, log_entries):
    with open(log_path, 'w') as log_file:
        log_file.write("\n".join(log_entries))

if __name__ == "__main__":
    image_path = r"no-red.png"
    output_path = r"no-red-marked.png"
    log_path = r"red-pixels-log.txt"

    result = count_and_mark_dominant_red_pixels(image_path, output_path, log_path)
    if result is not None:
        logging.info(f"The number of pixels with dominant red color: {result}")
        logging.info(f"Marked image saved to: {output_path}")
        logging.info(f"Log file saved to: {log_path}")