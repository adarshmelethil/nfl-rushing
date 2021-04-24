from nfl import db


SPECIAL_CHAR_MAPPING = {
    "_slash_": "/",
    "_percent": "%",
    "_plus": "+",
    "first": "1st",
    "twenty": "20",
    "forty": "40",
    "_percent": "%"
}


def reverse_mapping(m):
    return dict(zip(*list(zip(*m.items()))[::-1]))


class Rushing(db.Model):
    player = db.Column(db.String(64), primary_key=True)
    team = db.Column(db.String(3), primary_key=True)
    pos = db.Column(db.String(2), primary_key=True)

    att = db.Column(db.Integer)
    att_slash_g = db.Column(db.Float)
    yds = db.Column(db.String(64))
    avg = db.Column(db.Float)
    yds_slash_g = db.Column(db.Float)
    td = db.Column(db.Integer)
    lng = db.Column(db.String(32))
    first = db.Column(db.Integer)
    first_percent = db.Column(db.Float)
    twenty_plus = db.Column(db.Integer)
    forty_plus = db.Column(db.Integer)
    fum = db.Column(db.Integer)

    def __repr__(self):
        return f"{self.player} - {self.team} - {self.pos}"

    @staticmethod
    def swap_key(data, old, new):
        data[new] = data[old]
        del data[old]

    @staticmethod
    def colnames():
        return list(
            map(Rushing.key_to_table,
                map(lambda kv: kv[0],
                    filter(lambda kv: not kv[0].startswith("_")
                           and not callable(kv[1])
                           and '__func__' not in dir(kv[1]),
                           Rushing.__dict__.items()))))

    @staticmethod
    def key_to_dict(key):
        mapping = SPECIAL_CHAR_MAPPING
        for _from, _to in mapping.items():
            key = key.replace(_from, _to)

        key = "/".join(map(lambda l: l.capitalize(), key.split("/")))
        if key.lower() in ["td", "fum"]:
            key = key.upper()
        return key

    @staticmethod
    def key_to_table(key):
        mapping = reverse_mapping(SPECIAL_CHAR_MAPPING)
        key = key.lower()

        for _from, _to in mapping.items():
            key = key.replace(_from, _to)

        return key

    @staticmethod
    def table_dict(dict_vals):
        new_dict = {}
        for key, value in dict_vals.items():
            key = Rushing.key_to_dict(key)
            new_dict[key] = value
        return new_dict

    @staticmethod
    def from_dict(dict_vals):
        new_dict = Rushing.table_dict(dict_vals)
        return Rushing(**new_dict)

    def to_dict(self):
        new_dict = {}
        for key, value in self.__dict__.items():
            if key.startswith("_"):
                continue
            key = Rushing.key_to_table(key)

            new_dict[key] = value
        return new_dict
