import json
import pandas as pd
from corps_name import CorpName
from get_corpcode import Get_Corpcode
from get_corpcode import Get_Key

def Get_Codes(corps: list[str]) -> pd.DataFrame:
    
    try:
        print("CORPCODE.json 파일 읽어오는 중...\n")

        with open("CORPCODE.json", 'r') as f:
            json_data = json.load(f)
    except FileNotFoundError:
        print("CORPCODE.json 파일이 없습니다\n")
        print("CORPCODE.json 다운받는 중...\n")
        
        API_key = Get_Key()
        Get_Corpcode(key=API_key)

        print("CORPCODE.json 다운 완료\n")

        print("CORPCODE.json 파일 읽어오는 중...\n")
        with open("CORPCODE.json", 'r') as f:
            json_data = json.load(f)
    
    print("CORPCODE.json 파일 읽기 완료\n")

    corp_data = json_data['result']['list']

    df_corp = pd.DataFrame(corp_data)

    df_corp.set_index(['corp_name'], drop=True, inplace=True)

    return df_corp.loc[corps, :]

if __name__ == "__main__":
    corps = CorpName.sec_list

    data = Get_Codes(corps)

    print(data)

    # 코드가 2개인 회사들 modify_date 최신으로 변경
