from utils import config
from utils import logger
import traceback
from django.core.mail.backends.smtp import EmailBackend

local_logger = logger.local_logger('Client SMTP outbound mail',config.log_name,config.log_level)

class LoggingSmtp(EmailBackend):
	def _send(self, email_message):
		try:
			result = super(LoggingSmtp,self)._send(email_message)

			local_logger.info("Send succeeded: To: %s, From: %s, Message: %s, encoding: %s" % (
			','.join(email_message.recipients()),
				email_message.from_email,
				email_message.message().as_string(),
				email_message.encoding
				))

			return result
		except:
			local_logger.error("Send failed: %s: To: %s, From: %s, Message: %s, encoding: %s" % (
				traceback.format_exc(),
				','.join(email_message.recipients()),
				email_message.from_email,
				email_message.message().as_string(),
				email_message.encoding
				))
			
			raise
