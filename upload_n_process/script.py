import cgi
import subprocess

print("content-type: text/html")
print()

form = cgi.FieldStorage()
cmd=form.getValue("filename")

print(f'The value of state is {cmd}')