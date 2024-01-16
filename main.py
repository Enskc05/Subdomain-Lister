from tkinter import *
import requests
from tkinter import messagebox

FONT = ("Verdana", 20, "normal")


def subdomain_search():
    target = input_entry.get()
    text = input_text.get("1.0", END)

    if len(target) == 0 or len(text) == 0:
        messagebox.showerror(title="!!!ERROR!!!", message="Lütfen hedef ve metin bilgilerini girin")
    else:
        try:
            with open("subdomain.txt", "a") as data_file:
                data_file.write(f"\nSubdomain kontrolleri:\n{text}")

            def make_request(url):
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    return response

                except requests.exceptions.ConnectionError:
                    print(f"{url} için bağlantı hatası")

                except requests.exceptions.RequestException as e:
                    print(f"{url} için hata: {e}")

            found_subdomains = []
            words = text.split() 
            for word in words:
                url = "http://" + word + "." + target
                response = make_request(url)

                if response and response.status_code == 200:
                    found_subdomains.append(url)

            if found_subdomains:
                result_text = "\n".join(found_subdomains)
                result_label.config(text=f"Bulunan geçerli subdomain'ler:\n{result_text}")

                
                with open("subdomain_bulunanlar.txt", "w") as output_file:
                    output_file.write(result_text)
                    messagebox.showinfo("Bilgi", "Bulunan subdomain'ler 'subdomain_bulunanlar.txt' dosyasına kaydedildi.")
            else:
                result_label.config(text="Geçerli subdomain bulunamadı.")

        except FileNotFoundError:
            with open("mysecret.txt", "w") as data_file:
                data_file.write(f"\nSubdomain kontrolleri:\n{text}")
        finally:
            input_text.delete("1.0", END)


root = Tk()
root.title("Subdomain Arama")

input_label = Label(text="Hedef web sitesini girin", font=FONT)
input_label.pack()

input_entry = Entry(width=20)
input_entry.pack()

entry_label = Label(text="Metni girin ", font=FONT)
entry_label.pack()

input_text = Text(width=15, height=5)
input_text.pack()

search_button = Button(text="ARAMA", command=subdomain_search)
search_button.pack()

result_label = Label(text="", font=FONT)
result_label.pack()

root.mainloop()
