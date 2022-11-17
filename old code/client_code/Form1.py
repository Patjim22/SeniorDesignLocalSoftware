from ._anvil_designer import Form1Template
from anvil import *

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    self.name_1.text = ""
    self.name_2.text = ""
    self.id_1.text = ""
    self.id_2.text = ""