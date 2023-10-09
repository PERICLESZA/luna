class Customer:
    def __init__(self, 
                    idcustomer, 
                    name,   
                    phone, 
                    andress, 
                    fk_idcity, 
                    email, 
                    fk_ididentification, 
                    fk_idcustomer,
                    active,
                    fk_idclasscustomer,
                    zipcode,
                    state,
                    phone2,
                    dtbirth,
                    numidentification,
                    comissionpercent,
                    restriction,
                    attention,
                    picture_path,
                    
        ):
        self.idcustomer = idcustomer
        self.name = name
        self.phone = phone
        self.andress = andress
        self.fk_idcity = fk_idcity
        self.email = email
        self.fk_ididentification = fk_ididentification
        self.fk_idcustomer = fk_idcustomer
        self.active = active
        self.fk_idclasscustomer = fk_idclasscustomer
        self.zipcode = zipcode
        self.state = state,
        self.phone2 = phone2,
        self.dtbirth = dtbirth,
        self.numidentification = numidentification,
        self.comissionpercent = comissionpercent,
        self.restriction = restriction,
        self.attention = attention,
        self.picture_path = picture_path,
        

