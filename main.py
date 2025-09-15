import requests
import smtplib
from bs4 import BeautifulSoup
import os
import dotenv

dotenv.load_dotenv()

send_email= os.environ.get("SMTP_ADDRESS")
recieve_email= os.environ.get("EMAIL_ADDRESS")
password=os.environ.get("EMAIL_PASSWORD")   
connection = smtplib.SMTP("smtp.gmail.com")
connection.starttls()
connection.login(user=send_email,password=password)
response = requests.get("https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6", headers={"Accept-Language":"en-US,en;q=0.9","User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"})

soup= BeautifulSoup(response.text,"html.parser")

rands=soup.find(name="span",class_="a-price-whole").getText()
cents=soup.find(name="span",class_="a-price-fraction").getText()
title=soup.find(name="span",id="productTitle").getText()

# print(rands+cents)
# print(title.strip())

if int(rands.replace(".",""))<100:
    msg=f"Subject:Amazon Price Alert!!!\n\n{" ".join(title.split())} is now ${rands+cents}"
    connection.sendmail(from_addr=send_email,
                    to_addrs=recieve_email,
                    msg=msg.encode("utf-8")
                    )
    connection.close()


print("Done!!!")