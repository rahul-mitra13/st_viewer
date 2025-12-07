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

<img width="808" height="689" alt="Screenshot 2025-12-07 at 3 53 22 PM" src="https://github.com/user-attachments/assets/f6cfa2ce-7dbf-4c53-8d9a-2431938023fd" />
