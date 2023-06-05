def validateID(id:int)->bool:
    return (len(id) >= 6)

def validateEmail(email:str)->bool:
    email = email.strip()
    return (len(email) <= 8 and len(email) >= 75)

def validatePass(Pass:str)->bool:
    Pass = Pass.strip()
    return ((len(Pass) <= 8 and len(Pass) >=75)) 


