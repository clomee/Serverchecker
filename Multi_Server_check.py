import urllib.request
import time
import smtplib
import ssl

urls = {}
interval = 5


def menu():
    print("You are in the menu now.")
    command = str(input())
    if command == "add":
        set_url()
    elif command == "show":
        show_urls()
    elif command == "start monitoring":
        check_servers()
    else:
        menu()


def set_url():
    print("Name of the Webserver:")
    name = str(input())
    print("URL:")
    url = str(input())
    print("How many chars should i check for?")
    n = int(input())
    html = urllib.request.urlopen(url)
    basis_html = html.read(n).decode("utf8")
    html.close()
    print("URL:" + url)
    print("The first " + str(n) + " characters of your html are:")
    print(basis_html)
    print("Do your want to add this webserver to the List? y/n")
    if str(input()) == "y":
        urls[name] = (url, n, basis_html)
        menu()
    else:
        print("Webserver wasn´t added.")
        menu()


def show_urls():
    print(urls.keys())
    print("Done")
    menu()


def check_servers():
    for key in urls:
        server = urls[key]
        name = key
        url = server[0]
        n = server[1]
        comparative = server[2]
        html = urllib.request.urlopen(url)
        html_str = html.read(n).decode("utf8")
        html.close()
        if html_str == comparative:
            send_error_mail(name, url)
    time.sleep(interval)
    check_servers()
    menu()


def send_error_mail(name, url):
    file = open("accountdata.txt")
    email = file.readline()
    password = file.readline()
    recipient = file.readline()
    file.close()
    message = """
    Subject: Server inconsistency

    The HTML of {name} ({url}) is not like it should be.
    Please take a look at it!!""".format(url=url, name=name)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email, password)
        server.sendmail(email, recipient, message)


menu()
