from pydicom.uid import ExplicitVRLittleEndian
from pynetdicom import AE, debug_logger, evt
from pynetdicom.sop_class import CTImageStorage

"""
Let’s create a simple Storage SCP for receiving CT Image datasets encoded using the Explicit 
VR Little Endian transfer syntax. Create a new file my_scp.py, open it in a text editor and add 
the following:

$ python -m pynetdicom storescu 127.0.0.1 11112 image-00000.dcm-v -cx

"""

debug_logger()

def handle_store(event):
    """Handle EVT_C_STORE events."""
    ds = event.dataset
    ds.file_meta = event.file_meta
    ds.save_as(ds.SOPInstanceUID, write_like_original=False)

    return 0x0000

handlers = [(evt.EVT_C_STORE, handle_store)]

ae = AE()

'''
we create a new AE instance. However, because this time we’ll be the association acceptor, 
its up to us to specify what presentation contexts are supported rather than requested. 
Since we’ll be supporting the storage of CT Images encoded using the Explicit VR Little Endian transfer 
syntax we use add_supported_context() to add a corresponding presentation context.

'''
ae.add_supported_context(CTImageStorage, ExplicitVRLittleEndian)
ae.start_server(("127.0.0.1", 11112), block=True, evt_handlers=handlers)