from psychopy import visual

def create_scaled_image(win, image_path):
    img = visual.ImageStim(
        win,
        image=image_path,
        pos=(0, 0),
        units='norm'
    )
    
    # Get the image's aspect ratio
    # aspect_ratio = img.size[0] / img.size[1]
    
    # # Set height to 90% of window height and scale width accordingly
    # img.size = (2 * aspect_ratio, 2)  # Adjust 1.8 to change overall size
    
    return img
