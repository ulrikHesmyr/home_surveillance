def send_notification():
    print("Sent notification")

    #Send requests to the webserver to notify the user
    #OR
    #Send an email to the user from a separate thread


def reactivate_notification():
    global sent_notification

    sent_notification = False