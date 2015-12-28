from django.shortcuts import render, redirect
from forms import PolynomialForm
from django.forms import ValidationError
from . import polynomial_parser

from models import Polynomial

#
# def parser(request):
#     user_typed = None
#     standard_form = None
#     queryset = Polynomial.objects.all()
#
#     if queryset.exists():
#         p = queryset.first()
#         user_typed = p.polynomial
#         try:
#             standard_form = polynomial_parser.simplify(user_typed)
#         except ValueError:
#             pass
#         queryset.delete()
#         return render(request, 'projects/parser.html',
#                       {"user_typed": user_typed,
#                        "standard_form": standard_form})
#
#     if request.method == "POST":
#         p = Polynomial()
#         p.polynomial = request.POST['poly']
#         p.save()
#         return redirect('projects:parser')
#
#     return render(request, 'projects/parser.html', {})


def index(request):
    return render(request, 'projects/index.html', {})


def parser(request):

    poly = None
    form = PolynomialForm()

    if request.method == "POST":
        form = PolynomialForm(request.POST)
        if form.is_valid():
            try:
                request.session['poly'] = polynomial_parser.simplify(
                    form.cleaned_data['poly'])
            except IndexError:
                raise ValidationError("fart")

            return redirect('projects:parser')

    if 'poly' in request.session:
        poly = request.session['poly']
        del request.session['poly']

    return render(request, 'projects/parser.html', {'poly': poly,
                                                    'form': form,
                                                    'request': request})
