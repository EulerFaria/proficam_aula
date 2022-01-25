import logging


def get_logger( LOG_NAME='', 
        LOG_FORMAT     = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        DATE_FORMAT ="%Y-%m-%d %H:%M:%S",):
    """
    This generates a looger (i.e. Logging Object) with the configuration defined.
    - Stream Handler for showing the information on terminal
    - File Handler for saving the logs on a man.log file

    Parameters
    ----------
    LOG_NAME: String
        Name of the model in the following pattern: XXX_YYY_ZZZ where 
         .XXX_ is an abreviation to the business area name,
         .YYY_ is an abreviation to the product/model name,
         .XXX_ is an abreviation to the location which the product is running,

         e.g. MIN_PROD_CKS > Mine _ Productivity _ Carajás. 

    LOG_FORMAT: String 
        String for formatting the logger mesages. 
        E.g.
        2013-09-20 11:52:07 AM         INFO     This is an INFO message
        2013-09-20 11:52:07 AM         WARNING  This is a WARNING message
        2013-09-20 11:52:07 AM         ERROR    This is an ERROR message

    DATE_FORMAT: String
        Date format of the logging messages
    
    Returns
    ----------
    log: Object 
        Logging object with handlers and format adjusted
    """

    log           = logging.getLogger(LOG_NAME)
    log_formatter = logging.Formatter(fmt=LOG_FORMAT,datefmt=DATE_FORMAT)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_formatter)
    stream_handler.setLevel(logging.INFO)
    log.addHandler(stream_handler)

    file_handler = logging.FileHandler('main.log',encoding = "UTF-8")
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.DEBUG)
    log.addHandler(file_handler)


    log.setLevel(logging.DEBUG)

    return log

