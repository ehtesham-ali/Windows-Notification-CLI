# Importing modules
import argparse
import threading
import time
import winrt.windows.ui.notifications as notifications
import winrt.windows.data.xml.dom as dom

# Sleeper Thread Definition
def sleeper_thread(toast_class, timer):
    timer *= 60
    time.sleep(timer)
    print('Notification Executed. You may now close this Command Window')
    notifier.show(toast_class)

# Main
if __name__ == '__main__':
    # Initialize Parser + Parser Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('title', help='What you want your reminder\'s title to be?')
    parser.add_argument('body', help='This is where you add the information for the reminder')
    parser.add_argument('time', help='After how many minutes do you want the reminder to ring?')
    args = parser.parse_args()

    # Parser Results
    temp_title = args.title[:]
    toast_title = ''
    for char in temp_title:
        if char != '_':
            toast_title += char
        else:
            toast_title += ' '
    toast_body = args.body
    toast_timer = int(args.time[:])

    print(f'''
    Reminder Title: {toast_title}
    Reminder Body: {toast_body}
    Reminder Time: After {toast_timer} min(s)
    ''')

    # Create Toast Notifier
    nManager = notifications.ToastNotificationManager
    notifier = nManager.create_toast_notifier("<!--PYTHON APP-ID-->")

    # Defining Toast
    tString = f"""
    <toast scenario="Alarm" launch="app-defined-string">
        <audio src="ms-winsoundevent:Notification.Looping.Alarm" loop="true" />
        <visual>
            <binding template='ToastGeneric'>
                <text>{toast_title}</text>
                <text>{toast_body}</text>
            </binding>
        </visual>
        <actions>
            <action activationType="system" arguments="dismiss" content="" />
        </actions>
    </toast>
    """

    # Converting str to XML
    xDoc = dom.XmlDocument()
    xDoc.load_xml(tString)

    # Running Sleeper Thread
    thread = threading.Thread(target=sleeper_thread, args=(notifications.ToastNotification(xDoc), toast_timer))
    thread.start()
    thread.join()