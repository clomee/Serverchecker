import urllib.request
import time
import smtplib
import ssl
import os

urls = {}
interval = 5


def menu():
    print("You are in the menu now.")
    command = str(input())
    if command == "add":
        set_url()
    elif command == "show":
        show_urls()
    elif command == "start":
        check_servers()
    elif command == "export":
        export_servers()
    elif command == "import":
        import_servers()
    elif command == "commands":
        commands()
    elif command == "change":
        print("Which server do you wanna change?")
        changedelete()
    else:
        print(command + "is not a usable command, write commands to see all commands!")
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
        if html_str != comparative:
            send_error_mail(name, url)
    time.sleep(interval)
    check_servers()
    menu()


def send_error_mail(name, url):
    file = open("accountdata.txt", "r")
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


def export_servers():
    print("Name of the file:")
    filename = str(os.path.dirname(__file__))+"/"+str(input())+".txt"
    exported_data = open(filename, "a")
    for key in urls:
        exported_data.write(key+":"+str(urls[key])+"\n")
    exported_data.close()
    menu()


def import_servers():
    print("Insert the files path!")
    filepath = str(input())
    import_data = open(filepath, "r")
    count = len(import_data.readlines())
    # to be continued
    menu()


def commands():
    print(open("commandlist.txt", "r"))


def changedelete():
    f = str(input())
    for key in urls:
        if key == f:
            server = urls[key]
            name = key
            url = server[0]
            n = server[1]
            print("Do you want to change or delete the server? c/d")
            mode = str(input())
            if mode == "c":
                print("What do you wanna change? name, url, number of characters checked. xxn will change name and url, xnx will change name and the number of characters checked and so on...")
                code = str(input())
                if code[0] == "x":
                    print("enter a new name")
                    name = str(input())
                if code[1] == "x":
                    print("enter a new url")
                    url = str(input())
                if code[2] == "x":
                    print("How many characters should i check for?")
                    n = int(input())
                html = urllib.request.urlopen(url)
                basis_html = html.read(n).decode("utf8")
                html.close()
                urls[name] = (url, n, basis_html)
                del urls[key]
                menu()
            elif mode == "d":
                del urls[key]
                menu()
            else:
                print("This isn´t an option, please start again.")
                changedelete()
            menu()
    print("This server doesn´t exist in the list.")
    print("Please insert a valid servername.")
    changedelete()


menu()
