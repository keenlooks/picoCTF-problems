from hacksport.problem import Challenge, File
import string

class Problem(Challenge):
    files = [File("blackhole.img")]
    def setup(self):
        self.flag = "Hacking*Radiation"
