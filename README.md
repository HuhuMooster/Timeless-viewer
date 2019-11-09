# Timeless jewel viewer
### Requirements
- Python 3.6+
- MongoDB
- Python packages in `requirements.txt`

### Setup
1. Create a virtual environment with `python3 -m venv venv`
2. Activate the virtual environment by running `activate.bat`
3. Install python packages by running `install_reqs.bat`
4. Install a [MongoDB server](https://www.mongodb.com/download-center/community)
5. Install the accompanying database by extracting `project_timeless.json` and `timeless.json` from `databases.zip` and importing them to your Mongo database by running `import_db.bat`

### Usage
1. Run `run_site.bat` to start the flask app.
2. Open `http://127.0.0.1:5000/` in your browser.
3. Type in one of the following into the "Name" input field (it's case insensitive): 
    - Brutal Restraint
    - Elegant Hubris
    - Glorious Vanity
    - Lethal Pride
    - Militant Faith
4. "Seed" input field is optional. There are no checks applied to this field so be mindful of each jewel type seed number restrictions.
5. "Socket ID" input field is optional. Jewel socket positions reference image is at the top of the page.
6. After typing in the desired search options press enter or click the `Search` button.
6. A very simple website will display a list of added mods on the existing tree nodes (there may be some errors due to the issues with OCR in the jewel analyzer tool) and a list of summed values of all the tree nodes in the jewel radius.

### Examples
1. If you want to search for a Brutal Restraint #4243 jewel in all jewel sockets then you would type in the following:
    - `Brutal Restraint` in the "Name" input field
    - `4243` in the "Seed" input field
    - Leave the "Socket ID" input field empty
    - Press enter or click the `Search` button
2. If you want to search for all Lethal Pride jewels in jewel socket 12 (marauder jewel socket) then you would type in the following:
    - `Lethal Pride` in the "Name" input field
    - Leave the "Seed" input field empty
    - `12` in the "Socket ID" input field
    - Press enter or click the `Search` button
3. If you want to search for all Glorious Vanity jewels in all jewel sockets then you would type in the following:
    - `Glorious Vanity` in the "Name" input field
    - Leave "Seed" and "Socket ID" input fields empty
    - Press enter or click the `Search` button
