# windows debugging

These steps should be performed from a <u>**command prompt**</u>.  
`virtualenvwrapper` does <u>**not**</u> play well with powershell.
Be forewarned.

1.  Install python 3.6 and virtualenvwrapper-win

        choco install -y python3
        c:\python36\python.exe --version  # ensure 3.6.3 or higher
        c:\python36\scripts\pip.exe install virtualenvwrapper-win
        
        
2.  Create your virtual environment & install requirements

        cd c:\path\to\djenga
        mkvirtualenv djenga
        workon djenga
        pip install -r requirements.txt
        
                  
3.  Setup pycharm for debugging by pointing your project interpreter to
    `c:\users\username\envs\djenga\scripts\python3.6.exe`.  Create a 
    run configuration for celery by adding `manage.py` as the 
    script file, `c:\path\to\djenga` as the working directory, and
    `celery` as parameters.  You'll also need to add an env variable
    for celery to work correctly:
    
        FORKED_BY_MULTIPROCESSING=1

        