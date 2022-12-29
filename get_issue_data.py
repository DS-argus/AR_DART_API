import json
import xmltodict
import pandas as pd
import xlwings as xw

from io import BytesIO
from zipfile import ZipFile
from datetime import date, timedelta
from urllib.request import urlopen
from urllib.parse import urlencode

from corps_name import CorpName

from get_corpcode import Get_Corpcode
from get_corpcode import Get_Key

from get_codes import Get_Codes


#공시정보 > 공시검색 개발가이드
def Get_Issue_data(key: str, corp_code: str, bgn_de: str, end_de: str) -> pd.DataFrame:
    url_main = "https://opendart.fss.or.kr/api/list.json"
    params = {
        "crtfc_key": key,
        "corp_code": corp_code,
        "bgn_de": bgn_de,
        "end_de": end_de,
        "ast_reprt_at": "Y",
        "pblntf_ty": "C",
        "page_count": "100"
    }

    url = url_main + "?" + urlencode(params)

    result = urlopen(url)

    if result.status != 200:
        raise Exception("HTTP connection error")

    json_result = json.loads(result.read())
    
    return pd.DataFrame(json_result['list'])


def Get_Doc_data(key: str, rcept_no: str):
    url_main = "https://opendart.fss.or.kr/api/document.xml"
    params = {
        "crtfc_key": key,
        "rcept_no": rcept_no
    }
    
    url = url_main + "?" + urlencode(params)

    result = urlopen(url)

    zip_file = ZipFile(BytesIO(result.read()))

    xml_file = zip_file.read(zip_file.namelist()[0])
    xml_str = xml_file.decode('utf-8')

    dict_str = xmltodict.parse(xml_str)    
    json_str = json.dumps(xmltodict.parse(xml_str), indent=4, ensure_ascii=False)
    json_file_name = name.split(".")[0]

    return 

if __name__ == "__main__":
    API_key = Get_Key()
    # corp_code = Get_Codes("케이비증권", "corp_code")

    # # recent 1 week
    # bgn_de = (date.today() - timedelta(weeks=1)).strftime("%Y%m%d")
    # end_de = date.today().strftime("%Y%m%d")

    # data = Get_Issue_data(key=key,
    #                     corp_code=corp_code,
    #                     bgn_de=bgn_de,
    #                     end_de=end_de)

    # print(data)

    rcept_no = "20221227000417"

    print(Get_Doc_data(key=API_key, rcept_no=rcept_no))
