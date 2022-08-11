class FloatUrlParameterConverter:
    regex = '[0-9]+\.?[0-9]+'

    def to_python(self, value):
        return float(value)

    def to_url(self, value):
        return str(value)


class BooleanUrlParameterConverter:
    regex = "$"

    def to_python(self, value):
        return bool(value)

    def to_url(self, value):
        return str(value)


def str_to_bool(value):
    if value == "True":
        return True
    elif value == "False":
        return False
