# Building Segmentation
The aim of this project is to segment/mask buildings from the Aerial Imagery

## To run the website
1. Create a virtual environment
2. Install the required packages
3. Create a file `run.sh`:
    ```bash
    export FLASK_APP=app
    export FLASK_ENV=development
    export SECRET_KEY='secret key'
    export UPLOAD_FOLDER='/your/path/to/static'
    flask run
    ```
4. Turn the file `run.sh` into an executable:
    ```bash
    $ chmod +xrun.sh
    ```
5. Run the file: `./run.sh`