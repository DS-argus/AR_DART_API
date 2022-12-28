import json
import pandas as pd
from corps_name import CorpName
from get_corpcode import Get_Corpcode
from get_corpcode import Get_Key

def Get_Codes(corp: str, type: str, remove_duplicates: bool = True) -> str or pd.DataFrame:
    
    assert type == "corp_code" or "stock_code", "Check your code type"

    try:
        with open("CORPCODE.json", 'r') as f:
            json_data = json.load(f)
    except FileNotFoundError:
        print("CORPCODE.json does not exist\n")
        print("Downloading CORPCODE.json\n")
        
        API_key = Get_Key()
        Get_Corpcode(key=API_key)

        print("Download completed\n")

        print("Reading CORPCODE.json...\n")
        with open("CORPCODE.json", 'r') as f:
            json_data = json.load(f)

    corp_data_all = json_data['result']['list']

    df_corp = pd.DataFrame(corp_data_all)

    df_corp = df_corp[df_corp['corp_name'] == corp]

    # get a code with recent modify_date if corp_name is duplicated
    if remove_duplicates == True:

        df_corp.sort_values(by='modify_date', ascending=False, inplace=True)

        df_corp.drop_duplicates(subset='corp_name', keep='first', inplace=True)

    df_corp.set_index(['corp_name'], drop=True, inplace=True)
    
    return df_corp.loc[corp, type]


if __name__ == "__main__":
    sec_corps = CorpName.sec_list

    for corp in sec_corps:
        corp_code = Get_Codes(corp, "corp_code")
        stock_code = Get_Codes(corp, "stock_code")
        print(f"{corp} 기업코드 : {corp_code}")
        print(f"{corp} 주식코드 : {stock_code}")
