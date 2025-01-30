import os
import requests
from tkinter import Tk, Listbox, Button, MULTIPLE, END, messagebox
from tkinter.ttk import Frame
from msal import PublicClientApplication

# config app azure

CLIENTE_ID = 'cliente_ID'
AUTHORITY = 'https://login.microsoftonline.com/common'
SCOPE = ['Files.ReadWrite.All']

# iniciar app MSAL

app = PublicClientApplication(CLIENTE_ID, authority=AUTHORITY)

# autenticacao

def authenticate():
    result = None
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(SCOPE, account = accounts[0])
    if not result:
        flow = app.initiate_device_flow(scope=SCOPE)
        print(flow['message'])
        result = app.acquire_token_by_device_flow(flow)
    return result

# obter arquivos onedrive

def get_files(token):
    headers = {'Authorization': 'Bearer ' + token['access_token']}
    response = requests.get('https://graph.microsoft.com/v1.0/me/drive/root/children', headers=headers)
    return response.json().get('value', [])

# deleta arquivos selecionados
def delete_files(token, file_ids):
    headers = {'Authorization': 'Bearer ' + toke['access_token']}
    for file_id in file_ids:
        request.delete(f'https://graph.microsoft.com/v1.0/me/drive/items/{file_id}', headers=headers)

# interface grafica

class OneDriveApp(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.token = authenticate()
        self.files = get.files(self.token)
        self.populate_listbox()
    
    def create_widgets(self):
        self.listbox = Listbox(self, selectmode=MULTIPLE)
        self.listbox.pack()
        self.delete_button = Button(self, text="Delete Selected", command=self.delete_selected)
        self.delete_button.pack()

    def populate_listbox(self):
        for file in self.files:
            self.listbox.insert(END, file['name'])

    def delete_selected(self):
        selected_indices = self.listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Nada foi selecionado.", "Por favor, selecione arquivos para deletar")
            return
        files_ids = [self.files[i]['id'] for i in selected_indices]
        delete_files(self.token, files_ids)
        for i in reversed(selected_indices):
            self.listbox.delete(i)
        messagebox.showinfo("Deletados.", "Voce deletou com sucesso.")

if __name__ == '__main__':
    root = Tk()
    app = OneDriveApp(master==root)
    app.mainloop()

