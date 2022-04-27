

class EmailAddress:
    def __init__(self, address="", password=""):
        self.address = address
        self.password = password

    def parse(self, line=""):
        result = []
        if line:
            value = ""
            text = ""
            if ":" not in line:
                source = line.split("@")
                if len(source) != 2 or any(s in source for s in source) is None:
                    return None
                text = line
            else:
                array = line.split(":")
                if len(array) != 2 or any(s in array for s in array) is None:
                    return None
                text = array[0]
                value = array[1]
                array = text.split("@")
                if len(array) != 2 or any(s in array for s in array) is None:
                    return None

            if value:
                result = EmailAddress(text, value)
            else:
                result = EmailAddress(text)

        return result


if __name__ == '__main__':
    email_class = EmailAddress()
    with open("../../emails.txt", 'r') as f:
        emails = f.readlines()
    for lines in emails:
        print(EmailAddress().parse(lines))






