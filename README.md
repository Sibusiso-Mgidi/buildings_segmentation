# Building Segmentation
The aim of this project is to segment/mask buildings from the Aerial Imagery

## To run the Flask website
1. Create a virtual environment
    * Using pip:
        * Ensure you have virtualenv installed:
            ```bash
            pip install virtualenv
            ```
        * Create a virtual environment:
            ```bash
            virtualenv virtualenv_name
            ```
    * **Recommended** using conda:
        ```bash
        conda create --name ENVNAME python=3.6
        ```
2. Activate the environment
    * Using virtualenv:
        ```bash
        source virtualenv_name/bin/activate
        ```
    * Using conda:
        ```bash
        conda activate ENVNAME
        ```

3. Install the required packages
    * Using pip:
        ```bash
        pip install pip_requirements.txt
        ```
    * Using conda:
        ```bash
        conda env update -n ENVNAME --file conda_requirements.yml
        ```
4. Create a file `run.sh`:
    ```bash
    export FLASK_APP=app
    export FLASK_ENV=development
    export SECRET_KEY='secret_key'
    export UPLOAD_FOLDER='/your/path/to/static'
    flask run
    ```
5. Turn the file `run.sh` into an executable:
    ```bash
    $ chmod +x run.sh
    ```
6. Run the file `run,sh`to startup Flask:
    ```bash
    ./run.sh
    ```

**Note**: Prediction will not work without launching a TensorFlow Serving sever