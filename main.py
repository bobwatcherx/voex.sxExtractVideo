from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
from bs4 import BeautifulSoup
import re
import json
import base64

# app = FastAPI()
# templates = Jinja2Templates(directory="templates")

def process_link():
    URL = "https://voe.sx/egrivmdavdhn"

    html_page = requests.get(URL)
    soup = BeautifulSoup(html_page.content, 'html.parser')
    name_find = soup.find("title").text
    slice_start = name_find.index("Watch ") + 6
    name = name_find[slice_start:]
    slice_end = name.index(" - VOE")
    name = name[:slice_end]
    name = name.replace(" ","_")
    print(name)

    sources_find = soup.find_all(string = re.compile("var sources")) #searching for the script tag containing the link to the mp4
    sources_find = str(sources_find)
    #slice_start = sources_find.index("const sources")
    slice_start = sources_find.index("var sources")
    source = sources_find[slice_start:] #cutting everything before 'var sources' in the script tag
    slice_end = source.index(";")
    source = source[:slice_end] #cutting everything after ';' in the remaining String to make it ready for the JSON parser

    source = source.replace("var sources = ","")    #
    source = source.replace("\'","\"")                #Making the JSON valid
    source = source.replace("\\n","")                 #
    source = source.replace("\\","")     #

    strToReplace = ","
    replacementStr = ""
    source = replacementStr.join(source.rsplit(strToReplace, 1)) #complicated but needed replacement of the last comma in the source String to make it JSON valid
    source_json = json.loads(source) #parsing the JSON
    try:
        link = source_json["mp4"] #extracting the link to the mp4 file
        print(name)
        link = base64.b64decode(link) # idk what to do here, never found an url that uses this method
        print(link)
    except KeyError:
        try:
            link = source_json["hls"]
            
            # added base64 decode and convert to string
            link = base64.b64decode(link)
            link = link.decode("utf-8")
            print(link)
            name = name +'_SS.mp4'

        except KeyError:
            print("Could not find downloadable URL. Voe might have change their site. Check that you are running the latest version of voe-dl, and if so file an issue on GitHub.")
            quit()
    
    print("\n")
    return name, link

# @app.get("/", response_class=HTMLResponse)
# async def render_player(request: Request):
#     name, link = process_link()
#     return templates.TemplateResponse("index.html", {"request": request, "link": link})

process_link()
