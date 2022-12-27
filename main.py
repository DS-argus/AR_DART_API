import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
import webbrowser

#STEP 2 
auth_key="c15b9d9e1509c67880761adf96d3df46867b269f" #authority key
company_code="003450" #company code : KB증권
start_date="20221031"
params = {
    'crtfc_key': "c15b9d9e1509c67880761adf96d3df46867b269f",
    'corp_code': company_code
}

#STEP 3
url = "http://dart.fss.or.kr/api/search.xml?auth="+auth_key+"&crp_cd="+company_code+"&start_dt="+start_date+"&bsn_tp=A001&bsn_tp=A002&bsn_tp=A003"

#STEP 4
resultXML=urlopen(url)  #this is for response of XML
result=resultXML.read() #Using read method

#STEP 5
xmlsoup=BeautifulSoup(result,'html.parser')

#STEP 6
data = pd.DataFrame()

te=xmlsoup.findAll("list")

for t in te:
    temp=pd.DataFrame(([[t.crp_cls.string,t.crp_nm.string,t.crp_cd.string,t.rpt_nm.string,
        t.rcp_no.string,t.flr_nm.string,t.rcp_dt.string, t.rmk.string]]),
        columns=["crp_cls","crp_nm","crp_cd","rpt_nm","rcp_no","flr_nm","rcp_dt","rmk"])
    data=pd.concat([data,temp])

#STEP 7 
data=data.reset_index(drop=True)

#OPTIONAL
print(data)
# user_num=int(input("몇 번째 보고서를 확인하시겠습니까?"))
# url_user="http://dart.fss.or.kr/dsaf001/main.do?rcpNo="+data['rcp_no'][user_num]
# webbrowser.open(url_user)