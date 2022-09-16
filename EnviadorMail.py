import smtplib as smtp
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from ArmadorDatos import obtener_mensaje, obtener_mensaje_precios, obtener_nombres_reales_origen_destino


lista_vuelos_precios = obtener_mensaje_precios()
lista_vuelos = obtener_mensaje()
origen = obtener_nombres_reales_origen_destino()[0]
destino = obtener_nombres_reales_origen_destino()[1]

print(lista_vuelos_precios)

html_text = '''
<div style="background-color:#7bceeb;">
    <table height="100%" width="100%" cellpadding="0" cellspacing="0" border="0">
      <tr>
        <td valign="top" align="left" background="https://fondosmil.com/fondo/31175.jpg">

        <div 
          style="
          height: 30em;
          width: 86%;
          background-color: rgba(255,255,255,0.4);
          border:1px solid black;
          margin-right: 100px;
          margin-left: 100px;
          margin-top: 50px;" 
        ">

          <h1 style="
            text-align:center;
            color:black;
          ">Hola! <br>Vuelos más baratos desde ''' + origen + ''' hasta ''' + destino + '''</h1>

          <p style="
            margin-top: 45px;
            text-align:center;
            font-family:arial;
            font-weight: bold;
            color: black;
          ">Encontramos los vuelos más baratos correspondientes a tu búsqueda, abajo dejamos una
          lista mostrando los vuelos más baratos y los meses más baratos.<br>
          Además, hemos adjuntado archivos Excel con listas completas de precios filtrados tanto
          por precio como por fecha.
          </p>

        </div>
  
        </td>
      </tr>
    </table>
  </div>
'''

attachment_vuelos_fecha = "Vuelos ordenados por fecha.txt"
attachment_vuelos_precios = "Vuelos ordenados por precio.txt"

attachments_lista = [attachment_vuelos_fecha, attachment_vuelos_precios]

msg = MIMEMultipart()
msg['To'] = "octi123456@gmail.com"
msg['From'] = "baratovuelos365@gmail.com"
msg['Subject'] = "Vuelos baratos"

msg.attach(MIMEText(html_text, 'html'))  # add message body (text or html)

for i in attachments_lista:  # add files to the message
    file_path = i
    attachment = MIMEApplication(open(file_path, "rb").read(), _subtype="txt")
    attachment.add_header('Content-Disposition','attachment', filename=i)
    msg.attach(attachment)

s = smtp.SMTP('smtp.gmail.com')
s.connect('smtp.gmail.com', 587)
s.ehlo()
s.starttls()
s.ehlo()
s.login('baratovuelos365@gmail.com','bzxqzrrurbtcvpav')
s.sendmail(msg['From'], msg['To'], msg.as_string())
s.close()