export PATH=`pwd`:`pwd`/..:`pwd`/../django:`pwd`/../django/bin:`pwd`/captcha:`pwd`/mailer:$PATH
#echo "This is the django-admin utility you're using:"`which django-admin.py`
export PYTHONPATH=.:`pwd`:`pwd`/..:`pwd`/../django:`pwd`/../django/bin::`pwd`/captcha:`pwd`/mailer:$PYTHONPATH
#echo "Note: setting PYTHONPATH won't work for Apache/WSGI setup, but don't worry about that for now."
