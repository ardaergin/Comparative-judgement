import os
from psychopy import visual, event, core
import random
import numpy as np

# ------------- Load Images Dynamically -------------
image_folder = "data/images"
reference_image_name = "ref_image.png"

# Load all .png files from the folder
image_files = [f for f in os.listdir(image_folder) if f.endswith(".png")]

# Ensure the reference image exists
if reference_image_name not in image_files:
    raise ValueError(f"Reference image '{reference_image_name}' not found in the folder.")

# Separate reference image from comparative images
reference_image_path = os.path.join(image_folder, reference_image_name)
comparison_image_files = [img for img in image_files if img != reference_image_name]

# Ensure there are enough images for comparisons
if len(comparison_image_files) < 2:
    raise ValueError("Not enough images for comparisons. At least two comparison images are required.")

# Assign unique IDs to comparison images
image_ids = {i: img for i, img in enumerate(comparison_image_files)}

# ------------- Experiment Setup -------------
# Window setup
win = visual.Window(color="white", fullscr=False)

# Reference image
reference_image = visual.ImageStim(win, image=reference_image_path, pos=(0, 0.5), size=(0.5, 0.5))

# Comparison images
comparison_images = [
    visual.ImageStim(win, pos=(-0.5 + i, -0.5), size=(0.4, 0.4)) for i in range(2)
]

# Instructions
instructions = visual.TextStim(win, text="Press LEFT for the left image or RIGHT for the right image.", color="black")

# Response logging
results = []

# Adaptive algorithm variables
item_scores = np.random.rand(len(comparison_image_files))  # Initial random scores for items
item_pairs = [(i, j) for i in range(len(comparison_image_files)) for j in range(i + 1, len(comparison_image_files))]
random.shuffle(item_pairs)

# ------------- Main Experiment Loop -------------
instructions.draw()
win.flip()
event.waitKeys(keyList=["space"])  # Wait for participant to start

for pair in item_pairs:
    i, j = pair

    # Update images for the trial
    reference_image.draw()
    comparison_images[0].image = os.path.join(image_folder, image_ids[i])
    comparison_images[1].image = os.path.join(image_folder, image_ids[j])

    # Draw images
    for img in comparison_images:
        img.draw()

    win.flip()
    response = event.waitKeys(keyList=["left", "right", "escape"])

    # Log response
    if response == ["left"]:
        results.append((image_ids[i], image_ids[j], "i"))
        item_scores[i] += 1  # Increment score for selected image
    elif response == ["right"]:
        results.append((image_ids[i], image_ids[j], "j"))
        item_scores[j] += 1
    elif response == ["escape"]:
        break  # Exit experiment

    # Update adaptive algorithm (e.g., modify pair presentation probabilities)
    # Placeholder for integrating Bradley-Terry-Luce model or similar

print(results)

# ------------- End of Experiment -------------
end_message = visual.TextStim(win, text="Thank you for participating!", color="black")
end_message.draw()
win.flip()
core.wait(3)

win.close()
core.quit()

# Save results
output_file = "data/responses/results.csv"

# Ensure the directory exists
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Write the results to the file
with open(output_file, "w") as f:
    f.write("Pair,Response\n")  # Write the header
    for r in results:
        f.write(f"{r[0]}-{r[1]},{r[2]}\n")

print(f"Results saved to {output_file}")
