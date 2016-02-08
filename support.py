
seen = []

class CommonEqualityMixin(object):
    """ define a simple equals implementation for these value objects. """

    def __eq__(self, other):
        return hasattr(other, '__dict__') and isinstance(other, self.__class__) and self._dicts_equal(other)

    def __str__(Self):
        return super().__str__() + ':' + str(Self.__dict__)

    def __repr__(self):
        items = ("%s = %r" % (k, v) for k, v in self.__dict__.items())
        return "<%s: {%s}>" % (self.__class__.__name__, ', '.join(items))

    def _dicts_equal(Self, other):
        global seen
        p = (Self, other)
        if p in seen:
            raise ValueError("recursive call " + p)

        d1 = Self.__dict__
        d2 = other.__dict__
        try:
            seen.append(p)
            result = d1 == d2
        finally:
            seen.pop()
        return result

    def __ne__(Self, other):
        return not Self.__eq__(other)

