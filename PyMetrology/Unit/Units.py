####################################################################################################
# 
# PyMetrology - A Spice package for Python
# Copyright (C) Salvaire Fabrice 2014
# 
####################################################################################################

####################################################################################################
#
#  - unit suffix
#  - simplify .001
#
####################################################################################################

####################################################################################################

import numbers
import math

####################################################################################################

class Unit(numbers.Real):

    __power__ = 0
    __spice_suffix__ = ''
    __unit_suffix__ = ''

    ##############################################

    def __init__(self, value):

        if isinstance(value, Unit):
            if self.__power__ == value.__power__:
                self._value = value._value
            else:
                self._value =  float(value) / self.scale
        elif isinstance(value, int):
            self._value =  value # to keep as int
        else:
            self._value = float(value)

    ##############################################

    @property
    def power(self):
        return self.__power__

    ##############################################

    @property
    def scale(self):
        return 10**self.__power__

    ##############################################

    @property
    def value(self):
        return self._value

    ##############################################

    def clone(self):
        return self.__class__(self._value)

    ##############################################

    def is_same_scale(self, other):

        return isinstance(other, Unit) and self.__power__ == other.__power__

    ##############################################

    def convert_value(self, other):

        if self.is_same_scale(other):
            return other._value
        else:
            return float(other) / self.scale

    ##############################################

    def convert(self, other):
        
        return self.__class__(self.convert_value(other))

    ##############################################

    def __int__(self):

        return int(self._value * self.scale)

    ##############################################

    def __float__(self):

        return float(self._value * self.scale)

    ##############################################

    def __str__(self):

        return str(self._value) + self.__spice_suffix__

    ##############################################

    def __nonzero__(self):

        """True if self != 0. Called for bool(self)."""

        return self._value != 0

    ##############################################

    def __add__(self, other):

        """self + other"""

        new_obj = self.clone()
        new_obj._value += self.convert_value(other)

        return new_obj

    ##############################################

    def __radd__(self, other):

        """other + self"""

        return other.__add__(self)

    ##############################################

    def __neg__(self):

        """-self"""

        return self.__class__(-self._value)

    ##############################################

    def __pos__(self):

        """+self"""
        return self.clone()


    ##############################################

    def __sub__(self, other):

        """self - other"""

        new_obj = self.clone()
        new_obj._value -= self.convert_value(other)

        return new_obj

    ##############################################

    def __rsub__(self, other):

        """other - self"""

        return other.__sub__(self)

    ##############################################

    def __mul__(self, other):

        """self * other"""

        new_obj = self.clone()
        new_obj._value *= float(other)

        return new_obj

    ##############################################

    def __rmul__(self, other):

        """other * self"""

        return other.__mul__(self)

    ##############################################

    def __div__(self, other):

        """self / other without __future__ division

        May promote to float.
        """

        new_obj = self.clone()
        new_obj._value /= float(other)

        return new_obj

    ##############################################

    def __rdiv__(self, other):

        """other / self without __future__ division"""

        return other.__div__(self)

    ##############################################

    def __truediv__(self, other):

        """self / other with __future__ division.

        Should promote to float when necessary.
        """

        raise NotImplementedError

    ##############################################

    def __rtruediv__(self, other):

        """other / self with __future__ division"""

        raise NotImplementedError

    ##############################################

    def __pow__(self, exponent):

        """self**exponent; should promote to float or complex when necessary."""

        new_obj = self.clone()
        new_obj._value **= float(exponent)

        return new_obj

    ##############################################

    def __rpow__(self, base):

        """base ** self"""

        raise NotImplementedError

    ##############################################

    def __abs__(self):

        """Returns the Real distance from 0. Called for abs(self)."""

        return self.__class__(abs(self._value))

    ##############################################

    def __eq__(self, other):

        """self == other"""

        return float(self) == float(other)

    ##############################################

    def __ne__(self, other):

        """self != other"""

        # The default __ne__ doesn't negate __eq__ until 3.0.

        return not (self == other)

    ##############################################

    def __trunc__(self):

        """trunc(self): Truncates self to an Integral.

        Returns an Integral i such that:
          * i>0 iff self>0;
          * abs(i) <= abs(self);
          * for any Integral j satisfying the first two conditions,
            abs(i) >= abs(j) [i.e. i has "maximal" abs among those].
        i.e. "truncate towards 0".
        """

        raise NotImplementedError

    ##############################################

    def __divmod__(self, other):

        """divmod(self, other): The pair (self // other, self % other).

        Sometimes this can be computed faster than the pair of
        operations.
        """

        return (self // other, self % other)

    ##############################################

    def __rdivmod__(self, other):

        """divmod(other, self): The pair (self // other, self % other).

        Sometimes this can be computed faster than the pair of
        operations.
        """

        return (other // self, other % self)

    ##############################################

    def __floordiv__(self, other):

        """self // other: The floor() of self/other."""

        raise NotImplementedError

    ##############################################

    def __rfloordiv__(self, other):

        """other // self: The floor() of other/self."""

        raise NotImplementedError

    ##############################################

    def __mod__(self, other):

        """self % other"""

        raise NotImplementedError

    ##############################################

    def __rmod__(self, other):

        """other % self"""

        raise NotImplementedError

    ##############################################

    def __lt__(self, other):

        """self < other

        < on Reals defines a total ordering, except perhaps for NaN."""

        return float(self) < float(other)

    ##############################################

    def __le__(self, other):

        """self <= other"""

        return float(self) <= float(other)

    ##############################################

    def inverse(self, the_class=None):

        inverse = 1. / float(self)
        if the_class is None:
            return self.__class__(inverse / self.scale) # Fixme: to func?
        else:
            return the_class(inverse)

    ##############################################

    def canonise(self):

        # log10(10**n) = n    log10(1) = 0   log10(10**-n) = -n   log10(0) = -oo

        try:
            abs_value = abs(float(self))
            log = math.log(abs_value)/math.log(1000)
            # if abs_value >= 1:
            #     power = 3 * int(log)
            # else:
            #     if log - int(log): # frac
            #         power = 3 * (int(log) -1)
            #     else:
            #         power = 3 * int(log)
            power = int(log)
            if abs_value < 1 and (log - int(log)):
                power -= 1
            power *= 3
            unit = __power_to_unit__[power]
            return unit(float(self) / 10**power)
        except:
            return self

####################################################################################################

class tera(Unit):
    """ T Tera 1e12 """
    __power__ = 12
    __spice_suffix__ = 'T'

class giga(Unit):
    """ G Giga 1e9 """
    __power__ = 9
    __spice_suffix__ = 'G'

class mega(Unit):
    """ Meg Mega 1e6 """
    __power__ = 6
    __spice_suffix__ = 'Meg'

class kilo(Unit):
    """ K Kilo 1e3 """
    __power__ = 3
    __spice_suffix__ = 'k'

class milli(Unit):
    """ m milli 1e-3 """
    __power__ = -3
    __spice_suffix__ = 'm'

class micro(Unit):
    """ u micro 1e-6 """
    __power__ = -6
    __spice_suffix__ = 'u'

class nano(Unit):
    """ n nano 1e-9 """
    __power__ = -9
    __spice_suffix__ = 'n'

class pico(Unit):
    """ p pico 1e-12 """
    __power__ = -12
    __spice_suffix__ = 'p'

class femto(Unit):
    """ f femto 1e-15 """
    __power__ = -15
    __spice_suffix__ = 'f'

# class mil(Unit):
#     """ mil Mil 25.4e-6 """
#     __scale__ = 25.4e-6
#     __spice_suffix__ = 'mil'


__units__ = (tera,
             giga,
             mega,
             kilo,
             Unit,
             milli,
             micro,
             nano,
             pico,
             femto,
)
__power_to_unit__ = {unit.__power__:unit for unit in __units__}

####################################################################################################

class Frequency(Unit):

    ##############################################

    @property
    def period(self):
        return self.inverse(Period)

    ##############################################

    @property
    def pulsation(self):
        return self * 2 * math.pi

####################################################################################################

class Period(Unit):

    ##############################################

    @property
    def frequency(self):
        return self.inverse(Frequency)

    ##############################################

    @property
    def pulsation(self):
        return self.frequency.pulsation

####################################################################################################
# 
# End
# 
####################################################################################################
