from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import csv
import smtplib
import pandas as pd
from email.mime.text import MIMEText


class DataHandler:
    def __init__(self):
        super().__init__()

    def convert(self, data, links):
        list_data = []
        soup = BeautifulSoup(data.text, "html.parser")

        if links == "TimeOff/TimeOffMatrixNSE.aspx":
            soup_data = soup.find_all("table", style="BORDER-COLLAPSE: collapse")
        else:
            soup_data = soup.find_all(id="ctl00_ContentPlaceHolder1_dgJobPostings")

        for table_num, table in enumerate(soup_data):
            for tr in table.find_all("tr"):
                row = [
                    "".join(cell.stripped_strings) for cell in tr.find_all(["td", "th"])
                ]
                list_data.append(row)
            return list_data

    def compare(self, data, file):
        with open(file) as csv_fille:
            reader = csv.reader(csv_fille)
            output = list(reader)
            compared_list = [
                item for item in data + output if item not in data or item not in output
            ]
            return compared_list

    def updater(self, data, file):
        with open(file, "w") as f:
            writer = csv.writer(f)
            writer.writerows(data)

    def data_sender(self, data, email, key, subject):
        df = pd.DataFrame(data)
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(email, key)
            msg = MIMEText(df.to_html(index=None, header=False), "html")
            msg["Subject"] = "UPDATED: " + subject
            server.sendmail(email, email, msg.as_string())
