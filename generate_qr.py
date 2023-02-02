# Importing library
import qrcode
 
# Data to be encoded
data = 'https://liena29-evaluation-gema-evaluation-956czd.streamlit.app/'
 
# Encoding data using make() function
img = qrcode.make(data)
 
# Saving as an image file
img.save('evaluation.png')