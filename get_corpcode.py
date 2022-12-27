import json
import xmltodict

from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
from urllib.parse import urlencode

def Get_Key() -> str:
  loc = r"Key.json"

  with open(loc, 'r') as f:
    content = json.load(f)

  return content["Key"]

def Get_Corpcode(key):

  url_main = "https://opendart.fss.or.kr/api/corpCode.xml"
  params = {
      "crtfc_key": key
  }

  url = url_main + "?" + urlencode(params)

  result = urlopen(url)

  zip_file = ZipFile(BytesIO(result.read()))

  for name in zip_file.namelist():
    xml_file = zip_file.read(name)
    xml_str = xml_file.decode('utf-8')
    
    json_str = json.dumps(xmltodict.parse(xml_str), indent=4, ensure_ascii=False)
    json_file_name = name.split(".")[0]

    with open(json_file_name + ".json", 'w') as f:
        f.write(json_str) 


if __name__ == "__main__":

  API_key = Get_Key()
  Get_Corpcode(key=API_key)