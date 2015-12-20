import re
import polynomial_parser
from django import forms


bracket_re = re.compile("\([^\(]+?\)")
IMPOSSIBLES = {"++", "--", "**(", "xx",}
IMPOSSIBLES |= set("{}x".format(i) for i in range(10))
IMPOSSIBLES |= set("x{}".format(i) for i in range(10))
ALLOWED = {"1", "2", "3", "4", "5", "6", "7", "8", "9",
           "0", "x", "+", "*", " ", "-", "(", ")",}


class PolynomialForm(forms.Form):
    poly = forms.CharField(required=True,
                           error_messages={'required': "Please type something"})

    def clean(self):
        cleaned_data = super(PolynomialForm, self).clean()
        poly = cleaned_data.get("poly")

        d = {"(": 1, ")": -1}
        count = 0

        if not poly:
            return self.cleaned_data
        if "()" in poly:
            raise forms.ValidationError("Invalid format")
        for character in poly:
            if character not in ALLOWED:
                raise forms.ValidationError("Invalid character: {}".format(
                    character))
            count += d.get(character, 0)
            if count < 0:
                raise forms.ValidationError("Invalid bracketing")
        for substring in IMPOSSIBLES:
            if substring in poly:
                raise forms.ValidationError("Invalid format")
        if count:
            raise forms.ValidationError("Invalid bracketing")

        try:
            polynomial_parser.simplify(poly)
        except (IndexError, ValueError):
            raise forms.ValidationError("Invalid format")

        return self.cleaned_data