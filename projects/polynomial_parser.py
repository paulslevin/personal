"""
Executive function: simplify
Input: expression containing +,-,*,**,(,),x,0-9 that can be read as
a polynomial
Output: the expression in standard form
Example: "(x-1)*(x+1)" --> "x**2-1"
Link: http://www.checkio.org/mission/simplification/
"""
import re
import operator

bracket_re = re.compile("\([^\(]+?\)")
IMPOSSIBLES = {"++", "--", "**(", "xx", }
IMPOSSIBLES |= set("{}x".format(i) for i in range(10))
IMPOSSIBLES |= set("x{}".format(i) for i in range(10))
ALLOWED = {"1", "2", "3", "4", "5", "6", "7", "8", "9",
           "0", "x", "+", "*", " ", "-", "(", ")", }


def correct_input(string):
    d = {"(": 1, ")": -1}
    count = 0
    for character in string:
        if character not in ALLOWED:
            return False
        count += d.get(character, 0)
        if count < 0:
            return False
    for substring in IMPOSSIBLES:
        if substring in string:
            return False
    return True if count == 0 else False


def remove_minuses(expr):
    expr = expr.replace("-", "+-").replace("--", "+").replace("++", "+")
    return expr


def valid_brackets(expr):
    """
    Return True if the given expression has valid bracketing.
    :param expr:
    """
    count, b_dict = 0, {"(": 1, ")": -1}
    for c in expr:
        count += b_dict.get(c, 0)
    return count == 0


def get_until(expr, *args):
    """
    Return a tuple consisting of the given expression with valid bracketing,
    up to the characters specified in args, and the index at which it
    terminates.
    :param args:
    :param expr:
    """
    for i, c in enumerate(expr):
        if i > 0 and c in args and valid_brackets(expr[:i]):
            return i, expr[:i]
    return len(expr), expr


def dist(terms, expr):
    """
    Apply the distributive law (p1+...+pn)*expr=(p1*expr+...+pn*expr).
    :param expr:
    :param terms:
    """
    inner_terms = "+".join(term + "*" + expr for term in terms).replace(" ", "")
    return "(" + inner_terms + ")"


def erase_brackets(expr):
    """
    Remove the brackets to put the given expression in an easy-to-parse form.
    :param expr:
    """
    expr = remove_minuses(expr)

    while "(" in expr:
        # m will match the first pair of brackets which contain no brackets
        m = bracket_re.search(expr)
        # since the matched substring contains no brackets, we can split by "+"
        terms, first, last = m.group()[1:-1].split("+"), m.start(), m.end()
        # now remove the brackets if they are redundant
        if (expr[first - 1: first] in {"+", "(", ""} and
                expr[last: last + 1] in {"+", ")", ""}):
            expr = bracket_re.sub(m.group()[1: -1], expr, 1)
        # or use the distributive law
        elif expr[last: last + 1] == "*" and expr[last + 1: last + 2] != "*":
            i, v = get_until(expr[last + 1:], "+", ")")
            j = i + len(expr[: last]) + 1
            new_exp = dist(terms, v)
            expr = expr.replace(expr[first: j], new_exp, 1)
        # or get rid of indices
        elif expr[last: last + 2] == "**":
            i, v = get_until(expr[last + 2:], "+", "(")
            j = i + len(expr[: last]) + 2
            offset = len(str(v)) + 2
            expr = expr.replace(expr[first:j],
                                "*".join(expr[first: j - offset]
                                         for _ in range(int(v))))
        # or bring products to the right-hand-side of our pair
        elif expr[first - 1: first] == "*":
            i, v = get_until(expr[:first - 1][::-1], "+", "(")
            j = first - i - 1
            expr = expr.replace(expr[j: last], m.group() + "*" + v[::-1])
        # or negate brackets
        elif expr[first - 1: first] == "-":
            p_dict = {"+": "("}
            p_term = p_dict.get(expr[first - 2: first - 1], "+(")
            expr = expr.replace(expr[first - 1: last],
                                p_term + "+".join(
                                    "-" + term for term in terms
                                ) + ")", 1)
            # also get rid of any duplicate + or - signs
            expr = expr.replace("--", "+").replace("++", "+")
    # finally replace -x by -1*x to ease parsing
    expr = expr.replace("-x", "-1*x")
    return expr


def sort_term(term):
    """
    Return coefficient and degree of monomial.
    :param term:
    """
    subterms, ints = term.split("*"), []
    for t in sorted(subterms):
        t = t.replace("^", "**")
        if t[-1].isdigit():
            ints.append(int(t))
        else:
            break
    if ints:
        coefficient = reduce(operator.mul, ints)
    else:
        coefficient = 1
    index = subterms.count("x")
    return index, coefficient


def get_coeff_dictionary(poly):
    """
    Return a dictionary of indices and their coefficients.
    :param poly:
    """
    poly = erase_brackets(poly)
    poly = erase_indices(poly)  # we need the polynomial not to contain **
    terms = poly.split("+")
    sorted_terms = [sort_term(term) for term in terms]
    coeff_dict = {}
    for t in sorted_terms:
        if t[0] not in coeff_dict.keys():
            coeff_dict[t[0]] = t[1]
        else:
            coeff_dict[t[0]] += t[1]
    return coeff_dict


def erase_indices(poly):
    """
    Erase indices as long as the polynomial has no brackets
    :param poly:
    :return:
    """
    assert "(" not in poly
    if "**" not in poly:
        return poly
    if "+" in poly:
        terms = poly.split("+")
        for i, v in enumerate(terms):
            if "**" in v:
                terms[i] = erase_indices(v)
        return "+".join(terms)
    elif "**" in poly and poly.count("*") == 2:
        print poly
        j = poly.index("**")
        poly = "(" + poly[:j] + ")*" + poly[j + 1:]
        print poly
        return erase_brackets(poly)
    elif "**" in poly:
        poly = poly.replace("**", "^")
        terms = poly.split("*")
        terms = [erase_indices(term.replace("^", "**")) for term in terms]
        return "*".join(terms)


def simplify(poly):
    poly = poly.replace(" ", "")
    if not correct_input(poly):
        raise ValueError("Please put the input in the correct format!")
    terms, coeff_dict = [], get_coeff_dictionary(poly)
    degree = max(coeff_dict.keys())
    for i in range(0, degree + 1)[::-1]:
        coeff = coeff_dict.get(i, 0)
        if i == 0 and coeff:
            terms.append(str(coeff))
        elif coeff == 1 and i == 1:
            terms.append("x")
        elif coeff == 1:
            terms.append("x**{}".format(str(i)))
        elif coeff == -1 and i == 1:
            terms.append("-x".format(str(i)))
        elif coeff == -1:
            terms.append("-x**{}".format(str(i)))
        elif coeff != 0 and i == 1:
            terms.append("{}*x".format(coeff, str(i)))
        elif coeff != 0:
            terms.append("{}*x**{}".format(coeff, str(i)))
    final_poly = "+".join(terms).replace("+-", "-")
    if final_poly:
        return final_poly
    return "0"

print simplify("(x+3)*(x-3)**7")
