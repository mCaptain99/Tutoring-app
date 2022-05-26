from flask import flash
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, validators, IntegerField, SelectField, \
    BooleanField

from utils.category import CATEGORIES


class RegistrationForm(FlaskForm):
    username = StringField('Nazwa uzytkownika', [
        validators.Length(min=6, max=35, message="Nazwa użytkownika musi mieć od 4 do 35 znaków"),
        validators.regexp(r'[A-Za-z0-9_]+', message="Nazwa użytkownika może zawierać tylko litery, cyfry i znak _")])
    email = StringField('Email', [
        validators.Length(min=6, max=35, message="Email musi mieć od 4 do 35 znaków"),
        validators.Email(message="Niepoprawny format email")])
    password = PasswordField('Haslo',[
        validators.DataRequired(message="Pole hasło nie może być puste"),
        validators.Length(min=6, max=35, message="Hasło musi zawierać od 4 do 35 znaków"),
        validators.EqualTo('confirm', message='Hasło i potwierdzenie hasła muszą być takie same')])
    phone = StringField('Nr Telefonu', [
        validators.regexp(r'[0-9]{9}', message="Niepoprawny numer telefonu")])
    fullname = StringField('Imie i nazwisko', [
        validators.DataRequired(message='Pole imię i nazwisko nie może być puste'),
        validators.regexp(r'[A-Za-z\ \-]+', message="Imię i nazwisko może składać się tylko z liter i spacji")])
    confirm = PasswordField('Potwierdz haslo', [
        validators.DataRequired(message="Pole hasło nie może być puste"),
        validators.Length(min=6, message="Hasło musi zawierać od 4 do 35 znaków")])
    recaptcha = RecaptchaField()

    def validate(self, **kwargs):
        return self.username.validate(self) and self.password.validate(self) and self.confirm.validate(self) and \
               self.email.validate(self) and self.phone.validate(self) and self.fullname.validate(self) and self.recaptcha.validate(self)


class LoginForm(FlaskForm):
    username = StringField('Nazwa uzytkownika', [
        validators.Length(min=6, max=35, message="Nazwa użytkownika musi mieć od 4 do 35 znaków"),
        validators.regexp(r'[A-Za-z0-9_]+', message="Nazwa użytkownika może zawierać tylko litery, cyfry i znak _")])
    password = PasswordField('Haslo', [
        validators.DataRequired(message="Pole hasło nie może być puste"),
        validators.Length(min=6, max=35, message="Hasło musi zawierać od 4 do 35 znaków"),
    ])
    previous = StringField("")
    recaptcha = RecaptchaField()

    def validate(self, **kwargs):
        return self.username.validate(self) and self.password.validate(self) and self.recaptcha.validate(self)


class AdSearchForm(FlaskForm):
    title = StringField("Tytuł")
    price = IntegerField("Cena")
    author = StringField("Autor")
    category = StringField('Kategoria', validators=[
        validators.AnyOf(CATEGORIES, message="Wybierz wartość z listy")])
    city = StringField("Miasto")
    radius = IntegerField("Promień")
    online = BooleanField("Online", default=False)
    stationary = BooleanField("Stacjonarnie", default=False)
    sort = SelectField('Payload Type', choices=[(1, "Ocena (od najwyższej)"), (2, "Cena (od najniższej)"),
                                                (3, "Tytuł (alfabetycznie)"), (4, "Data utworzenia (od najnowszej)")])

    def clean_data(self, **kwargs):
        ret = {}
        for kwarg in kwargs:
            if kwargs[kwarg]:
                ret[kwarg] = kwargs[kwarg]
        return ret

    def validate(self, **kwargs):
        return self.title.validate(self) and self.city.validate(self)\
               and self.category.validate(self)


class AdCreationForm(FlaskForm):
    title = StringField("Tytuł", validators=[
        validators.Length(min=3, max=35, message="Tytuł musi mieć od 4 do 35 znaków"),
        validators.DataRequired(message="Pole tytuł nie może być puste")])
    price = IntegerField("Cena")
    body = StringField("Treść Ogłoszenia", validators=[
        validators.Length(max=10000, message="Za długa wiadomość"),
    ])
    city = StringField('Miasto')
    category = StringField('Kategoria', validators=[
        validators.AnyOf(CATEGORIES, message="Wybierz wartość z listy")])
    online = BooleanField("Online", default=False)
    stationary = BooleanField("Stacjonarnie", default=False)
    recaptcha = RecaptchaField()

    def validate(self, **kwargs):
        return self.title.validate(self) and self.price.validate(self) and self.city.validate(self) and \
               self.category.validate(self) and self.recaptcha.validate(self)


class ReviewCreationForm(FlaskForm):
    body = StringField("Treść", validators=[
        validators.Length(max=10000, message="Za długa wiadomość"),
    ])
    rate = IntegerField("Ocena", validators=[
        validators.AnyOf([1, 2, 3, 4, 5], message="Ocena musi być liczbą z przedziału od 1 do 5")])
    recaptcha = RecaptchaField()

    def validate(self, **kwargs):
        return self.rate.validate(self) and self.body.validate(self) and self.recaptcha.validate(self)


class ResponseCreationForm(FlaskForm):
    body = StringField("Treść", validators=[
        validators.Length(max=10000, message="Za długa wiadomość"),
    ])
    review_id = StringField()
    recaptcha = RecaptchaField()

    def validate(self, **kwargs):
        return self.body.validate(self) and self.recaptcha.validate(self)


class UserEditForm(FlaskForm):
    phone = StringField("Numer telefonu", [
        validators.regexp(r'[0-9]{9}', message="Niepoprawny format numeru telefonu")])
    full_name = StringField("Imie i nazwisko", validators=[
        validators.DataRequired(message='Pole imię i nazwisko nie może być puste'),
        validators.regexp(r'[A-Za-z\ \-]+', message="Imię i nazwisko musi składać się tylko z liter, cyfr i spacji")])

    def validate(self, **kwargs):
        return self.phone.validate(self) and self.full_name.validate(self)


class PasswordResetForm(FlaskForm):
    reset_token = StringField('reset-token')
    password = PasswordField('Haslo', [
        validators.DataRequired(message="Pole hasło nie może być puste"),
        validators.Length(min=6, max=35, message="Hasło musi zawierać od 4 do 35 znaków"),
        validators.EqualTo('confirm', message='Hasło i potwierdzenie hasła muszą być takie same')])
    confirm = PasswordField('Potwierdz haslo', [
        validators.DataRequired(message="Pole hasło nie może być puste"),
        validators.Length(min=6, message="Hasło musi zawierać od 4 do 35 znaków")])
    recaptcha = RecaptchaField()

    def validate(self, **kwargs):
        return self.password.validate(self) and self.confirm.validate(self) and self.recaptcha.validate(self)


class PasswordForgotForm(FlaskForm):
    email = StringField('Email', [
        validators.Length(min=6, max=35, message="Email musi mieć od 4 do 35 znaków"),
        validators.Email(message="Niepoprawny format email")])
    recaptcha = RecaptchaField()

    def validate(self, **kwargs):
        return self.email.validate(self) and self.recaptcha.validate(self)


def show_error_messages(form: FlaskForm):
    for field in form.data:
        for error in form.__getattribute__(field).errors:
            flash(error)
