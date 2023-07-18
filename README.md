# TOOLS
Some tools created and used by myself

## Color Extract
### Extract 5 main colors from your image

1. Install dependent
```
pip install pillow numpy scikit-learn
```
2. Run the program
```
python ColorExtract.py image.jpg
```
3. Result will save as image_colorCode.jpg

Output:
![Imgur](https://i.imgur.com/eyekLvn.jpg)

## Film Color Palette
### Extract main colors from film

1. In Anaconda
```
conda create -n myenv python=3.8
conda activate myenv
```
2. Install dependent
```
conda install -c conda-forge opencv numpy scikit-learn pillow
```
3. Run the program
```
python FilmColorPalette.py <file_path> <num_colors>
```
4. Result will save as <film_name>_colorBar.jpg

Output:
![Imgur](https://i.imgur.com/7pC75I3.png)

## ConvertMarkdownImageLinks2imgur
### Convert every image link in your Markdown file to Imgur links.

1. Fill your Imgur API client_id and client_secret in code below.
```
client_id = 'Your Client ID'
client_secret = 'Your Client Secret'
```
2. Rename your Markdown file to new_markdown_file.md
3. Install imgurpython
```
pip install imgurpython
```
4. Run the program
```
python ConvertMarkdownImageLinks2imgur.py
```

Due to the speed limit of Imgur, only 50 uploads per IP per hour. You need to change your IP when you see the warning message.

## NASA Blue Marble Image Process
### Combine all 8 seperated NASA Blue Marble Images(21600 x 21600, due to the resaulation limit of image file) into one(86400 x 43200).

Example image: https://visibleearth.nasa.gov/images/73884/november-blue-marble-next-generation-w-topography-and-bathymetry

1. Download all 8 part images(A1, A2, B1, B2, C1, C2, D1, D2) in one folder.
2. Download NASABlueMarbleImageProcess.py into the same folder.
3. Install dependent
```
conda install -c conda-forge opencv numpy
```
4. Run the program
```
python NASABlueMarbleImageProcess.py [any 1 of the 8 image file names]
```

Attention: It would take up to 20GB of RAM of your computer, make sure you have enough free RAM.
