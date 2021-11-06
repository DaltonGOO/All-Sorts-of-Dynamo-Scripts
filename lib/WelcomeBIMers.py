
# used for opening github and website from python
import webbrowser


def hellowWorld():
    return "Hello, BIMers!"


class Website:
    github_link = "https://github.com/DaltonGOO"
    tbc_blog_link = "https://daltongoodwin.tech/"
    codewars_link = "https://www.codewars.com/users/The%20BIM%20Coordinator"

    def github (self):
        webbrowser.open_new(self.github_link)
    def tbc_blog (self):
        webbrowser.open_new(self.tbc_blog_link)
    def codewars (self):
        webbrowser.open_new(self.codewars_link)