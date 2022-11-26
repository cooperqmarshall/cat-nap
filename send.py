from smtplib import SMTP
from email.message import EmailMessage
from email.utils import make_msgid
import mimetypes
from os import environ


def format_message(img: bytes, img_url: str):
    msg = EmailMessage()
    msg['Subject'] = 'Cat of the Day'
    msg['From'] = environ['CAT_NAP_SENDER']
    msg['To'] = environ['CAT_NAP_RECIEVER']
    msg.set_content(f'Enjoy your cat of the day ;)!\n{img_url}')

    # now create a Content-ID for the image
    image_cid = make_msgid(domain='xyz.com')
    # if `domain` argument isn't provided, it will use your computer's name

    msg.add_alternative(f'''
    <html>
        <body>
        <p>Enjoy your cat of the day ;)</p>
        <img src="cid:{image_cid[1:-1]}">
        </body>
    </html>
    ''', subtype='html')
    # image_cid looks like <long.random.number@xyz.com>
    # to use it as the img src, we don't need `<` or `>`
    # so we use [1:-1] to strip them off
    # know the Content-Type of the image
    maintype, subtype = mimetypes.guess_type(img_url)[0].split('/')
    msg.get_payload()[1].add_related(img,
                                     maintype=maintype,
                                     subtype=subtype,
                                     cid=image_cid)
    return msg


def send_message(msg: EmailMessage, host: str, port: int):
    '''
    Sends an EmailMessage from the CAT_NAP_SENDER environment variable using
    the host and port params for the smtp session. The SENDER_PASSWORD
    envireonment variable is required to preform the smpt login 

    :params
        msg: an instance of EmailMessage
        host: the name of the remote host to which to connect
        port: the port to which to connect
    '''
    with SMTP(host=host, port=port) as smtp:
        smtp.starttls()
        smtp.login(environ['CAT_NAP_SENDER'], environ['SENDER_PASSWORD'])
        smtp.send_message(msg)
