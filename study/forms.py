from django import forms
from .models import Study
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

class StudyForm(forms.ModelForm):

    content = forms.CharField(
        error_messages={
            "required": "学習内容を入力してください。"
        }
    )

    class Meta:
        model = Study
        fields = ["content","tags"]

    def clean_content(self):
        content = self.cleaned_data["content"]

        # 前後の空白を取り除く
        content = content.strip()

        # 空白しか入力されていなかった場合
        if not content:
            raise ValidationError(
                "学習内容を入力してください。"
            )

        # 3文字以下だった場合
        if len(content) <= 3:
            raise ValidationError(
                "学習内容は4文字以上入力してください。"
            )

        return content

    def clean_tags(self):
        tags = self.cleaned_data["tags"]
        if len(tags) > 2:
            raise ValidationError(
                "タグは2つまで選択できます。"
            )
        
        return tags

class SignupForm(UserCreationForm):
    username = forms.CharField(
        error_messages={
            "required": "ユーザー名を入力してください。",
            "unique": "このユーザー名は既に使用されています。",
        }
    )

    password1 = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput,
        help_text="""
        8文字以上で設定してください。
        数字だけのパスワードや、よく使われるパスワードは使用できません。
        """,
    )

    password2 = forms.CharField(
        label="パスワード確認",
        widget=forms.PasswordInput,
        help_text="確認のため、同じパスワードをもう一度入力してください。",
        error_messages={
                        "required": "確認用パスワードを入力してください。",
                        }
    )   