<h1 align='center'><b>Synchronize Folders</b></b></h1>
This program synchronizes two folders: 'Source' and 'Replica'. The program maintains a full, identical copy of Source folder at Replica folder and performs a periodic synchronization.
File creation/copying/removal operations are logged to a file 'operations.log' and also in the console output;
<br><br>
<strong>How does it work</strong>
<br>

*To illustrate, we will use the 'Source' and 'Replica' folders that already exist in the file, but you can create other folders with different names and run the program using their 
folders as parameters, with the original folder being the first parameter and the destination folder being the second parameter.*

When you start the program, it starts the synchronization process. From then on, any file created in the 'Source' folder will be copied to the 'Replica' folder, and any changes/removals
files from 'Source' will be replicated in the 'Replica' folder.
<br><br>
<strong>Usage</strong>
<br />

```bash
python3 synchronizes_folders.py compare_files Source Replica
```
<br>
<strong>Pytest install</strong>
<br />
Create and activate the virtual environment:

```bash
python3 -m venv .venv && source .venv/bin/activate
```

Install *Pytest* with the command:
```bash
pip install pytest==7.3.1
```

Run the tests with the command:

```bash
pytest
```
