import os
os.system("python server2.py &")
os.system("sh setup")
from ghost import Ghost
ghost = Ghost()

with ghost.start() as session:
    page, extra_resources = ghost.open("http://chat.stackexchange.com/rooms/30332/beep-boop-maggot")
    assert page.http_status==200
    session.evaluate_js_file("client.js")