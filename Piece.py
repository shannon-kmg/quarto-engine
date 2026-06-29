class Piece:
    def __init__(self, q, uppercase, overline, underline):
        self.q = q
        self.uppercase = uppercase
        self.overline = overline
        self.underline = underline

        self.type_bitmask = 0
        if self.q: self.type_bitmask += 1
        if self.uppercase: self.type_bitmask += 2
        if self.overline: self.type_bitmask += 4
        if self.underline: self.type_bitmask += 8

    def __repr__(self):
        return self.draw()
    def draw(self):
        c = ""
        if self.overline:
            c += "\u0305"
        if self.underline:
            c += "\u0332"
        if self.q:
            if self.uppercase:
                c += "Q"
            else:
                c += "q"
        else:
            if self.uppercase:
                c += "G"
            else:
                c += "g"
        return c
