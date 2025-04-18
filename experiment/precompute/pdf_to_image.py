import fitz  # PyMuPDF
import os
import glob

def convert_pdf_to_images(pdf_path, output_format="png", dpi=288):
    doc = fitz.open(pdf_path)
    zoom = dpi / 72  # Converting DPI to scaling factor (default PDF DPI is 72)
    matrix = fitz.Matrix(zoom, zoom)
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(matrix=matrix, alpha=False)  # Rendering page to image
        
        if page_num == 0:
            output = f"texts/0_experiment_info.{output_format}"
        if page_num == 1:
            output = f"texts/4_practice_instructions.{output_format}"
        if page_num == 4:
            output = f"texts/5_trial_instructions_sim.{output_format}"
        if page_num == 5:
            output = f"texts/5_trial_instructions_sim_visual.{output_format}"
        if page_num == 2:
            output = f"texts/6_trial_instructions_liking.{output_format}"
        if page_num == 3:
            output = f"texts/6_trial_instructions_liking_visual.{output_format}"
        pix.save(output)
        print(f"Saved: {output}")
    
    doc.close()

if __name__ == '__main__':
    # Find the first (and presumably only) PDF file in the instructions directory
    pdf_files = glob.glob("instructions/*.pdf")
    if not pdf_files:
        raise FileNotFoundError("No PDF files found in the instructions directory")
    if len(pdf_files) > 1:
        print("Warning: Multiple PDF files found. Using the first one.")
    
    convert_pdf_to_images(pdf_files[0], output_format="png", dpi=432)
