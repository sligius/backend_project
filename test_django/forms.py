from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from django import forms
from .models import Review, UserRequest


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('critic', 'book', 'content')


class RequestForm(forms.ModelForm):
    class Meta:
        model = UserRequest
        fields = ['request_type', 'author_name', 'book_title']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('request_type', css_class='form-control-m rounded mb-3', label_class='h5'),
            Field('author_name', css_class='form-control-m rounded mb-3', label_class='h5'),
            Field('book_title', css_class='form-control-m rounded mb-3', label_class='h5'),
            Submit('submit', 'Отправить', css_class='btn btn-m mt-3 mb-0 p-2 rounded-pill btn-light')
        )

    def clean(self):
        cleaned_data = super().clean()
        request_type = cleaned_data.get('request_type')
        book_title = cleaned_data.get('book_title')

        if request_type == 'B' and not book_title:
            self.add_error('book_title', 'Поле с названием книги обязательно для заполнения при заявке на книгу.')
