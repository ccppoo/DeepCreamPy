from configparser import ConfigParser
import os

class Language:

    def __init__(self):

        self.language_code = "eng"
        self.language_name = "English"

        self.language_sets = dict()
        self.codes = list()
        self.names = list()

        self.__read_from_files()

    def __getattr__(self, item : str) -> str:
        lang_set = self.language_sets.get(self.language_name)
        if lang_set is None:
            print("exception")
            raise Exception('translation file problem :: ' + os.path.basename(__file__))

        return eval("\""+str(lang_set.get(item))+"\"")

    def set_language(self, code : str) -> None:
        self.language_code = code

    '''
    Updates all of the strings in *.ini file that exists
    if some string is not translated or left as blank
    default language, English, will be replaced for that string

    Parameters
    code (str) : language code (ISO-639-2), should be same as file name (e.g. English -> eng.ini )
    '''
    def __read_from_files(self) -> None:
        sep = '/'
        loc = os.path.dirname(__file__) + sep +'translations'
        files = [x for x in os.listdir(os.path.dirname(__file__) +'/translations') if x.endswith(".ini") and not x.startswith('sample')]

        for file_name in files:
            cp = ConfigParser()
            cp.read(loc + sep + file_name, encoding="utf-8")

            if not "language_info" in cp.sections() or not "strings" in cp.sections():
                continue

            code = cp.get("language_info", "code")
            name = cp.get("language_info", "name")
            self.codes.append(code)
            self.names.append(name)
            langSet = Language_set(code, name)

            for x in cp.options('strings'):
                langSet.setString(x, cp.get('strings', x))

            self.language_sets[name] = langSet


class Language_set:
    def __init__(self, code : str, name : str):
        self.strings = dict()
        self.code = code
        self.name = name

    def get(self, key):
        return self.strings.get(key)

    def __repr__(self):
        return 'class < Language_set({}, {}) >'.format(self.code, self.name)

    def setString(self, key : str, value : str) -> None:
        self.strings[key] = value

    def show(self):
        for k, v in self.__dict__.items():
            print(k, " : ", v)

if __name__ == "__main__":
    h = Language()
    h.set_language('kor')
    print(h.tutorial)
