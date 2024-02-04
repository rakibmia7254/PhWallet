import customtkinter as ctk
import pyperclip
import tkinter.messagebox as tkmb

from web3 import Web3
import requests

bsc_testnet_url = "https://data-seed-prebsc-1-s1.binance.org:8545/"
w3 = Web3(Web3.HTTPProvider(bsc_testnet_url))


def get_bnb_balance(wallet_address):
    balance = w3.eth.get_balance(wallet_address)
    return w3.from_wei(balance, 'ether')

def get_address(sender_private_key):
    sender_address = w3.eth.account.from_key(sender_private_key).address
    return sender_address


def send(receiver_address, amount, sender_private_key):
    sender_address = w3.eth.account.from_key(sender_private_key).address
    nonce = w3.eth.get_transaction_count(sender_address)
    transaction = {
    'to': receiver_address,
    'value': w3.to_wei(amount, 'ether'),
    'gas': 21000,
    'gasPrice': w3.to_wei('5', 'gwei'),
    'nonce': nonce,
    'chainId': 97
    }
    signed_transaction = w3.eth.account.sign_transaction(transaction, sender_private_key)
    transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    while True:
        try:
            transaction_receipt = w3.eth.get_transaction_receipt(transaction_hash)
            return w3.to_hex(transaction_receipt['transactionHash'])
            break
        except:
            pass

def get_tx(addr):
    data = []
    url=f"https://api-testnet.bscscan.com/api?module=account&action=txlist&address={addr}&sort=asc"
    txdata = requests.get(url).json()
    for i in txdata['result']:
        to=i['to']
        frm=i["from"]
        amn=i['value']
        if len(to)>0:
            if int(amn)>0:
                if to.lower()==addr.lower():
                    data.append({"type":"received","to":to,"from":frm,"amount":amn})
                else:
                    data.append({"type":"sent","to":to,"from":frm,"amount":amn})
            else:
                pass
        else:
            pass
    return data



ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("600x600")
app.iconbitmap('icon.ico')
app.title('PhWallet')

pk=None

if pk==None:
    dialog = ctk.CTkInputDialog(text="Enter Your PrivateKey: ", title="Import Wallet")
    pk = dialog.get_input()
else:
    pass

address = get_address(pk)
balance = get_bnb_balance(address)
tx=get_tx(address)[::-1]

def copyaddress():
    pyperclip.copy(address)
    copy_button.configure(text="Copied")
def send_c():
    addr=user_addr.get()
    amn=user_amn.get()
    tx=send(addr,amn,pk)
    tkmb.showinfo("Done", "TX_Hash "+str(tx))

def home():
    home_button.configure(fg_color='#0c7791')
    rcv_button.configure(fg_color='gray')
    send_button.configure(fg_color='gray')
    e_button.configure(fg_color='gray')
    home_frame.pack(fill=ctk.BOTH,pady=20)
    send_frame.pack_forget()
    rcv_frame.pack_forget()
    about.pack_forget()


def c_send():
    send_button.configure(fg_color='#0c7791')
    home_button.configure(fg_color='gray')
    rcv_button.configure(fg_color='gray')
    e_button.configure(fg_color='gray')
    send_frame.pack(pady=20)
    rcv_frame.pack_forget()
    home_frame.pack_forget()
    about.pack_forget()

def rcv():
    rcv_button.configure(fg_color='#0c7791')
    home_button.configure(fg_color='gray')
    send_button.configure(fg_color='gray')
    e_button.configure(fg_color='gray')
    send_frame.pack_forget()
    rcv_frame.pack(pady=20)
    home_frame.pack_forget()
    about.pack_forget()
    
def nn():
    home_button.configure(fg_color='gray')
    rcv_button.configure(fg_color='gray')
    send_button.configure(fg_color='gray')
    e_button.configure(fg_color='#0c7791')
    home_frame.pack_forget()
    about.pack(fill=ctk.BOTH,pady=20)
    send_frame.pack_forget()
    rcv_frame.pack_forget()


opt = ctk.CTkFrame(app)
opt.pack(pady=0)
opt.configure(width=600, height=35)
home_button = ctk.CTkButton(opt, text='Home', fg_color='#0c7791',command=home)
home_button.place(x=0,y=3)
send_button = ctk.CTkButton(opt, text='Send', fg_color="gray", command=c_send)
send_button.place(x=150,y=3)
rcv_button = ctk.CTkButton(opt, text='Receive', fg_color='gray',command=rcv)
rcv_button.place(x=300,y=3)
e_button = ctk.CTkButton(opt, text='About', fg_color='gray',command=nn)
e_button.place(x=450,y=3)

top_frame = ctk.CTkFrame(app)
top_frame.pack(pady=20)


label = ctk.CTkLabel(top_frame,text="PthWallet",font=("Bold", 25)) 
label.grid(row=0, column=0,padx=10) 
label = ctk.CTkLabel(top_frame, text='Network: BNB Testnet',font=("Arial", 13)) 
label.grid(row=0, column=1,padx=10)
label = ctk.CTkLabel(app, text='Your Assets: '+str(balance)[:7]+' BNB',font=("Arial", 15)) 
label.pack(pady=12,padx=10) 


home_frame = ctk.CTkScrollableFrame(app,
	orientation="vertical",
	width=300,
	height=200,
	label_text="Transection History",
	label_font=("Helvetica", 18),
	label_anchor = "center", # "w",  # n, ne, e, se, s, sw, w, nw, center,,,
	scrollbar_button_color="pink",
	scrollbar_button_hover_color = "gray",
	corner_radius = 20
)

home_frame.pack(fill=ctk.BOTH,pady=40)
if len(tx)>4:
    for x in tx:
        to_f=f"{x['to'][:4]}....{x['to'][::-1][:4][::-1]}"
        from_f=f"{x['from'][:4]}....{x['from'][::-1][:4][::-1]}"
        amount_f=float(x['amount'])/10**18
        text=f"{x['type']} : TO:{to_f}, From:{from_f}, Amount:{amount_f}"
        ctk.CTkLabel(home_frame, text=text).pack(pady=10)
else:
    ctk.CTkLabel(home_frame, text="No Transection").pack(pady=10)

send_frame = ctk.CTkFrame(app)
rcv_frame = ctk.CTkFrame(app)
about = ctk.CTkFrame(app)


user_addr = ctk.CTkEntry(send_frame,placeholder_text="Address")
user_addr.pack(pady=12,padx=10)
user_amn = ctk.CTkEntry(send_frame,placeholder_text="Amount")
user_amn.pack(pady=12,padx=10)
sendbb = ctk.CTkButton(send_frame, text='Send', command=send_c)
sendbb.pack(pady=12,padx=10)


label = ctk.CTkLabel(rcv_frame,text="Your Address: ",font=("Bold", 20))
label.pack(pady=20)
label = ctk.CTkLabel(rcv_frame, text=address,font=("Arial", 15))
label.pack(pady=12,padx=10) 
copy_button = ctk.CTkButton(rcv_frame, text="Copy", command=copyaddress)
copy_button.pack(pady=10)

decs= """Welcome to the BNB Testnet Wallet, a project crafted by Rakib Hossain.
 This wallet allows you to seamlessly interact 
 with the Binance Smart Chain Testnet, 
providing a user-friendly interface built 
with customtkinter and web3."""

label = ctk.CTkLabel(about,text="BNB Testnet Wallet by Rakib Hossain",font=("Bold", 20))
label.pack(pady=20)
label = ctk.CTkLabel(about,text=decs,font=("Bold", 15))
label.pack(pady=20)


app.mainloop()