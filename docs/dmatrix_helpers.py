
def save_matrix(dmatrix, file_name):
    dmatrix.save_binary(file_name)
    with open(file_name, 'rb') as f:
        xgb_data = f.read()
        return xgb_data
    
def write_binary(xgb_data, file_name):
    with open(file_name, 'wb') as f:
        f.write(xgb_data)
