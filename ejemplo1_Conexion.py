from pynetdicom import AE, debug_logger

#Escribiendo mi ptimer SCU con la libreria pynetdicom

# Antes de iniciar se tiene que iniciar el la aplicación  echoscp que viene con pynetdicom, 
# pero también se puede utilizar 
# cualquier aplicación de terceros que admita el servicio de verificación como SCP, como storescp de DCMTK.

# En una nueva terminal, inicie echoscp escuchando solicitudes de conexión en el puerto 11112 con el 
# indicador -v verbose (o puede usar el indicador -d debug para obtener aún más resultados):

# en la terminal usar: 
# python -m pynetdicom echoscp 11112 -v

# Se inicia el debug para visualizar informacion sobre el estado de la conexión 

debug_logger()

ae = AE() # creates a new AE instance
ae.add_requested_context("1.2.840.10008.1.1")


# Todas las solicitudes de asociación deben contener al menos un contexto de presentación y, 
# en este caso, hemos propuesto uno con la sintaxis abstracta para el servicio de verificación.
# "1.2.840.10008.1.1"

# Más adelante 
# analizaremos los contextos de presentación y cómo se utilizan para definir los servicios de una asociación.

#  SONIC_WALL                         187.188.96.139
#  SERVER GLOBAL   AE cmissemymFIR    172.40.68.6      port 2104
#  SERVER LOCAL    AE cmistolFIR      172.40.68.10     port 2104
#  DATA CENTER                        10.150.0.11

# "127.0.0.1", 11112

assoc = ae.associate("127.0.0.1", 11112)


#T he AE.associate() method returns an Association instance assoc, which is a subclass of threading.Thread. 
# This allows us to make use of the association while pynetdicom monitors the connection behind the scenes

# Verificacion del estado de la conexión

# Accepts the association and replies with an A-ASSOCIATE-AC message. However, 
# just because an association has been accepted doesn’t mean that the proposed services have also been accepted.
# Rejects the association by replying with an A-ASSOCIATE-RJ message.
# Aborts the association negotiation by sending an A-ABORT message.

if assoc.is_established:
    print("Association established with Echo SCP!")
    status = assoc.send_c_echo()
    assoc.release()
else:
    # Association rejected, aborted or never connected
     print("Failed to associate")

     # Si a activado el debug por que se extiende la infoacion entregada 

     # I: Information about the state of the association and services
     # E: Errors and exceptions that have occurred
     # D: The contents of various association related messages, such as the A-ASSOCIATE-RQ and A-ASSOCIATE-AC 
     # messages, as well as summaries of exchanged DIMSE messages (not shown here)

     