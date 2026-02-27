import streamlit_custome_css as leo


def mail_send(re_id,na,us,pas):

    sender_mail = "pythonleo637@gmail.com"
    receiver_mail = re_id
    subject = "Register in smart attendance system"
    name=na
    user_name=us
    password_us=pas
    body =f'''HI {name}  you are register in attendance system 
            your details:
                        username:{user_name}
                        password:{password_us}
                                        Thank you!'''
    password = "dttp oczk lhik geoy"

    leo.mail(sender_mail,receiver_mail,subject,body,password)