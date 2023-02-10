from fastapi    import FastAPI
from typing     import Union
from imaplib    import IMAP4_SSL
from bs4        import BeautifulSoup          as bs


def Hotmail(mail,password):
    try:  
        msrvr = IMAP4_SSL('outlook.office365.com', 993)
        msrvr.login(mail, password)
        homthu = ['junk','inbox']
        for hom in homthu:
            stat,cnt = msrvr.select(hom)
            try:
                stat,dta = msrvr.fetch(cnt[0], '(BODY[TEXT])')
                soup = bs(dta[0][1], "html.parser")
                try:
                    link = str(soup).split('''Verify email address''')[1].split()[1]
                except:
                    link = None
                try:
                    msrvr.store(cnt[0], '+FLAGS', '\\Deleted')
                except:
                    pass
                data_out = {'link':link}
            except:
                data_out = {'link':None}
    except Exception as e:
        print(e)
        if 'LOGIN failed' in str(e):
            data_out = {'link':False}
        else:
            data_out = {'link':None}
    return data_out

app = FastAPI()


@app.get("/")
async def root():
    return {
        "status": "success",
        "message": "TL SOFTWARE"
    }

@app.get("/api/v1/get-code-openai")
def read_item(mail: Union[str, None] = None, passMail: Union[str, None] = None):
    if not mail or not passMail:
        return {'status': "error", "msg": "Không được để trống tham số"}
    else:
       get = Hotmail(mail, passMail)
       return {'status': "success", 'link': get['link']}
