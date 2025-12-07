# Purpose: 

A simple "stitch file" viewer such as those created by [Autoknit](https://github.com/textiles-lab/autoknit) which implements the paper 
[Automatic Machine Knitting of 3D Meshes](https://textiles-lab.github.io/publications/2018-autoknit/).

# Usage 

All the requirements are listed in `requirements.txt`. Here are the build instruction in Linux/MacOS systems. I recommend making a virtual enviroment. 

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 viewStitchFile.py [.st file]
```

# Output 

[Polyscope](https://polyscope.run/) is used to render the output.

