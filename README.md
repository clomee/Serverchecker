# Serverchecker

The Serverchecker is a tool to observate your own or your clients webservers based of the HTML it returnes.
It will notify you when something changed.

To start your serverchecker, you need to have an gmail account wich can be used to send this emails.
Just replace the first and second line in the accountdata.txt with your accountname and password.
The third line needs to be replaced with the email you want the notifications sent to.

After that, just start the script and add servers with the "add" function.
Give it a name, url and how many characters of the html it should check for.

with the "start monitoring" command it starts, if you dont want to check each 5 seconds just edit the interval variable in the 7th line.
When you stop it, all observated servers will be deletet.
