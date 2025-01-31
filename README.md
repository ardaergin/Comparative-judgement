# Comparative Judgement Research

This is the repository for comparative judgement research.

## Installation for Mac

For Mac, you must first download **Homebrew**. Homebrew is a tool that helps you install software like Python on your Mac.

I also recommend downloading and installing **GitHub Desktop** (you must have a GitHub account). Once you have GitHub Desktop, clone this repository by clicking the green "Code" button at the top of this page and selecting "Open with GitHub Desktop".

Once the repository is cloned, you must open Terminal and navigate to the location of the cloned repository. Here’s how:

1. Open GitHub Desktop.
2. Right-click on the repository name in the left panel, and click **"Reveal in Finder"**.
3. In Finder, select **View > Show Path Bar**.
4. You will see a path displayed at the bottom of the Finder window. Right-click the "Comparative-judgement" folder in this path bar and select **"Copy \"Comparative-judgement\" as Pathname"**.
5. Open Terminal.
6. Type `cd` (leave a space after `cd`), then paste the copied pathname. It should look like `cd /Users/yourname/path/to/Comparative-judgement`. Press Enter.

Once you are in the correct directory, run the following commands one at a time in Terminal:

```bash
brew install python@3.10
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> **Note:** While you can copy and paste all commands at once, it is recommended to run them line by line to check for any errors.

Once these installations are done, you must create an `images` folder under the `Comparative-judgement` folder yourself with the following structure (and you must put the images used in the study in these folders yourself):

```
images/
├── practice/
│   ├── comparison/
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   ├── image3.jpg
│   │   └── ...
│   └── reference/
│       └── ref_image.jpg
├── trials/
│   ├── comparison/
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   ├── image3.jpg
│   │   └── ...
│   └── reference/
│       └── ref_image.jpg
```

**`images/`**: Root folder for all images used in the experiment.
  - **`practice/`**: Folder for practice-related images.
    - **`comparison/`**: Must contain multiple images used as comparison stimuli for practice trials.
    - **`reference/`**: Must contain exactly one image used as the reference for practice trials.
  - **`trials/`**: Folder for main trial-related images.
    - **`comparison/`**: Must contain multiple images used as comparison stimuli for main trials.
    - **`reference/`**: Must contain exactly one image used as the reference for main trials.

> **Important Note**: The program will load and process images based on their folder location, not based on their name. Hence, the image names can be anything you want, but the folder names must follow the structure described above.


## Installation for the Lab

1. **Install Git**:
   - Download and install Git from [this link](https://git-scm.com/).
   - After installation, open **Git Bash**. This is a program that provides a Unix-like environment for Git commands. The window name will start with `MINGW64`.

2. **Set Up the Shared Folder**:
   - Since we want to share the repository across all lab computers:
     1. Open **File Explorer**.
     2. Right-click **This PC** and select **Map Network Drive**.
     3. Choose `Z:` as the drive letter and enter the network path:
        ```
        \\vu.local\home\FA_FEWEB-RESEARCH002\Files
        ```
     4. Click **Finish**.

3. **Navigate to the Correct Folder**:
   - In Git Bash, change the directory to the shared folder:
     ```bash
     cd /z/11-cubicle
     ```
   - Replace `11-cubicle` with the name of the folder you want. Tip: Type the first few letters of the folder name and press **Tab** to autofill the name.

4. **Clone the Repository**:
   - Run the following command to copy the repository to the shared folder:
     ```bash
     git clone https://github.com/ardaergin/Comparative-judgement.git
     ```

5. **Set Up Python**:
   - Install Python 3.10.11 from [this link](https://www.python.org/downloads/release/python-31011/).

6. **Set Up the Experiment**:
   - Once Python is installed, navigate to the repository folder in Git Bash and run:
     ```bash
     python3.10 -m venv .venv
     source .venv/Scripts/activate
     pip install -r requirements.txt
     ```
    - This sets up the virtual environement that is used for running the experiment, and downloads the required libraries like `psychopy`.

## Updating the Repository

To update the local copy of the repository in the lab with the latest changes from the server:

1. Navigate to the repository folder in Git Bash:
   ```bash
   cd Z:
   cd 11-cubicle
   cd Comparative-judgement
   ```

2. Run the following command:
   ```bash
   git pull origin main
   ```

This command fetches the latest updates from the main branch of the repository.

> **Tip:** If you encounter any errors during this update, double-check that you are in the correct folder.
