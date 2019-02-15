# modification of code from http://naelshiab.com/tutorial-send-email-python/
import smtplib
import csv

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

path_to_csv = '/home/srini/Downloads/767_a1.tsv'
delimiter = '\t'
fromaddr = "srinivas.venkattaramanujam@mcgill.ca"
password = ""  # WARNING REMOVE PASSWORD BEFORE COMMIT!!!!!!!!!!!!!!!!!!!!!!

graded_by = 'Q1a) Sitao/Martin, Q1b) Harsh, Q2a) Srini Q2b) Riashat'
ta_emails = '\nHarsh Satija harsh.satija@mail.mcgill.ca\nSitao Luan sitao.luan@mail.mcgill.ca\nSrinivas Venkattaramanujam sri.venkattaramanujam@mail.mcgill.ca\nMartin Klissarov martin.klissarov@mail.mcgill.ca\nRiashat Islam riashat.islam@mail.mcgill.ca'
with open(path_to_csv) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=delimiter)
    line_count = 0
    for row in csv_reader:
        if line_count == 0 or line_count == 1:
            print('ignoring: {}'.format(row))
            pass
        else:
            print('row:', row)

            toaddr = row[1].replace('#', '')

            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = "COMP 767-A1 feedback"
            scores = [0, 0, 0, 0]
            for i in range(2, 6):
                try:
                    scores[i-2] = int(row[i])
                except:
                    pass
            body = "Scores: Q1:{}/50 Q2:{}/50 \nFeedback:\nQ1: {} \nQ2: {}\n\nPlease DO NOT REPLY to this email. For questions" \
                   " about the feedback contact the TA who graded the question[{}].\nThe TA emails are: {} \n\nThanks, \nSrinivas".format(scores[0]+scores[1], scores[2]+ scores[3],
                                                                              row[8]+' '+row[9],row[10]+' '+row[11], graded_by, ta_emails)
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.office365.com', 587)
            server.starttls()
            server.login(fromaddr, password)
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            server.quit()
        line_count += 1
    print('Processed {} lines.'.format(line_count))

