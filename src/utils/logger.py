import logging
import smtplib
import time
import traceback
import pprint
import socket
import datetime

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# User has to call setLogger() and optionally setSMTP(), 
# if use_smtp is set to True.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

HOSTNAME=socket.gethostname()

class CustomFormatter(logging.Formatter):
    def format(self, record):
        newmsg = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
            datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S"),
            HOSTNAME,
            record.levelname,
            record.name,
            record.filename,
            record.lineno,
            record.msg,
            record.exc_info if record.exc_info else '',
            record.exc_text if record.exc_text else ''
            )
        return newmsg

class CustomLogging(logging.getLoggerClass()):
    '''
    No constructor here. It is problematic to call the parent's 
    constructor, because we're inheriting from a local instance
    of a global object.
    '''

    def setLogger(self,app_or_class,file,logger_level,use_smtp):
        self.logger_app_or_class = app_or_class
        self.logger_file = file
        self.logger_level = logger_level
        self.use_smtp = use_smtp

    def setSMTP(self,server,port,login,password,tls,smtp_debug_level,from_addr,to_addrs):
        self.smtp_server = server
        self.smtp_port = port
        self.smtp_login = login
        self.smtp_password = password
        self.smtp_tls = tls
        self.smtp_debug_level = smtp_debug_level
        self.smtp_from_addr = from_addr
        self.smtp_to_addrs = to_addrs

    def critical(self, msg, *args, **kwargs):
        new_msg = msg % args if args else msg
        if self.use_smtp:
                if self.passedInitTest():
                        self.sendAlert(new_msg,self.smtp_from_addr,self.smtp_to_addrs.split(','))

        self._log(logging.CRITICAL, msg, args, kwargs)

    def passedInitTest(self):
        if not hasattr(self,'smtp_server'):
            msg = " CustomLogging.sendAlert(): Cannot send alerts: User needs to call setSMTP() to set outbound email parameters."
            self._log(logging.CRITICAL, msg, None, None)
            return False
        return True

    def sendAlert(self,msg,from_addr,to_addrs):
        if not self.use_smtp:
            msg = " CustomLogging.sendAlert(): SMTP was OFF when this logger was intialized. Turn it on and call setSMTP() to change this behavior."
            self._log(logging.CRITICAL, msg, None, None)
            return

        if not self.passedInitTest():
            return

        server = smtplib.SMTP(self.smtp_server,self.smtp_port)
        server.set_debuglevel(self.smtp_debug_level)
        retry=3
        while retry > 0:
            try: 
                server.ehlo()
                if self.smtp_tls:
                    server.starttls()
                    server.ehlo()
                server.login(self.smtp_login,self.smtp_password)
                server.sendmail(from_addr, to_addrs, msg)
                retry=0
            except:
                errstring =  " CustomLogging.sendAlert(): Error: Send failed, RETRYING, " + str(retry) + " retries left, msg:" + msg + ", recipients:" + pprint.pformat(to_addrs) + " Traceback:" + traceback.format_exc() 
                self._log(logging.CRITICAL, errstring, None, None)
                retry -= 1
                time.sleep(5)
        try: 
            server.quit()
        except:
            pass

def local_logger(app_or_class,logfile,use_smtp=True,level=logging.DEBUG):
    use_name = app_or_class
    if not isinstance(app_or_class,str):
        use_name = app_or_class.__name__

    logger = CustomLogging(use_name)
    logger.setLogger(use_name,logfile,level,use_smtp)
    logger.setLevel(level)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(logfile)
    fh.setLevel(level)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(level)
    # create formatter and add it to the handlers
    formatter = CustomFormatter("%(asctime)s %(name) %(levelname) %(message)s")
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger

def log_save_diff(collection,logger,method,obj):
	return
	if '_id' in obj.__dict__:
		orig_obj = (method)(collection, obj._id)
		logger.info("Saving %s.\nCurrent:\n%s\nNew:\n%s\n" % (str(obj.__class__), pprint.pformat(orig_obj.__dict__), pprint.pformat(obj.__dict__)) )
	else:
		logger.info("Saving %s.\nFirst time:\n%s" % (str(obj.__class__), pprint.pformat(obj.__dict__)) )
	print "Saved by:"
	for n in traceback.format_list(traceback.extract_stack()[12:]):
		print "%s\n" % n

    
if __name__ == "__main__":
    l = local_logger('my_app','./log_test.log',logging.DEBUG)

    # "application" code
    l.debug("debug message")
    l.info("info message")
    l.warn("warn message")
    l.error("error message")
    l.critical("critical message")

    from config import ConfigFile
    config = ConfigFile()
    l.setSMTP(config.smtp.server,config.smtp.port,config.smtp.login,config.smtp.password,config.smtp.tls,config.smtp.debug_level,config.smtp.from_addr,config.smtp.to_addrs)
    l.critical("critical message")

