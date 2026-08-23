from django.test import TestCase
from .models import Study
from django.contrib.auth import get_user_model
from .forms import StudyForm
from django.urls import reverse
from .models import Study, Tag


class StudyFormTest(TestCase):

    # 正しい学習内容を入力した場合、バリデーションを通過することを確認
    def test_valid_content(self):
        form = StudyForm(
            data={
                "content": "Pythonを勉強する"
            }
        )

        self.assertTrue(form.is_valid())


    # 短すぎる学習内容を入力した場合、バリデーションエラーになることを確認
    def test_short_content(self):
        form = StudyForm(
            data={
                "content": " a "
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)


    # 空白のみの学習内容を入力した場合、バリデーションエラーになることを確認
    def test_whitespace_only_content(self):
        form = StudyForm(
            data={
                "content": "   "
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)

    # タグ2個ならStudyFormのバリデーションを通過することを確認
    def test_two_tags_are_valid(self):
        tag1 = Tag.objects.create(name="Python")
        tag2 = Tag.objects.create(name="Django")

        form = StudyForm(
            data={
                "content": "PythonとDjangoを勉強する",
                "tags": [tag1.id, tag2.id],
            }
        )

        self.assertTrue(form.is_valid())

    # タグ3個ならStudyFormのバリデーションエラーになることを確認
    def test_three_tags_are_invalid(self):
        tag1 = Tag.objects.create(name="Python")
        tag2 = Tag.objects.create(name="Django")
        tag3 = Tag.objects.create(name="AWS")
        
        form = StudyForm(
            data={
                "content": "PythonとDjangoを勉強する",
                "tags": [tag1.id, tag2.id , tag3.id],
            }
        )
        
        self.assertFalse(form.is_valid())
        self.assertIn("tags", form.errors)


class StudyModelTest(TestCase):

    # 各テストで使用するダミーユーザーを作成
    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="testuser",
            password="testpass"
        )


    # Studyを作成し、内容とユーザーが正しくDBに保存されることを確認（Create）
    def test_create_study(self):
        study = Study.objects.create(
            content="Pythonを勉強する",
            user=self.user
        )

        self.assertEqual(Study.objects.count(), 1)
        self.assertEqual(study.content, "Pythonを勉強する")
        self.assertEqual(study.user, self.user)


    # 既存Studyのcontentを変更し、DBにも更新内容が保存されることを確認（Update）
    def test_update_study(self):
        study = Study.objects.create(
            content="Pythonを勉強する",
            user=self.user
        )

        study.content = "Djangoを勉強する"
        study.save()

        study.refresh_from_db()

        self.assertEqual(study.content, "Djangoを勉強する")


    # Studyを削除した場合、DBから対象データが削除されることを確認（Delete）
    def test_delete_study(self):
        study = Study.objects.create(
            content="Pythonを勉強する",
            user=self.user
        )

        self.assertEqual(Study.objects.count(), 1)

        study.delete()

        self.assertEqual(Study.objects.count(), 0)


    # ユーザーに紐づくStudyをDBから取得できることを確認（Read）
    def test_read_study(self):
        Study.objects.create(
            content="Pythonを勉強する",
            user=self.user
        )

        study = Study.objects.get(
            user=self.user
        )

        self.assertEqual(study.content, "Pythonを勉強する")

    # Studyにタグを追加し、関連が正しく保存されることを確認
    def test_add_tags_to_study(self):
        study = Study.objects.create(
            content="Pythonを勉強する",
            user=self.user
        )

        tag1 = Tag.objects.create(name="Python")
        tag2 = Tag.objects.create(name="Django")

        study.tags.add(tag1, tag2)

        self.assertEqual(study.tags.count(), 2)
        self.assertIn(tag1, study.tags.all())
        self.assertIn(tag2, study.tags.all())

class StudyViewTest(TestCase):

    # 認証・Viewテストで使用するダミーユーザーを作成
    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="testuser",
            password="testpass"
        )

        self.other_user = User.objects.create_user(
            username="otheruser",
            password="otherpass"
        )


    # 正しいユーザー名・パスワードでログインできることを確認
    def test_login_success(self):
        logged_in = self.client.login(
            username="testuser",
            password="testpass"
        )

        self.assertTrue(logged_in)


    # 未ログイン状態でDashboardへアクセスした場合、Login画面へリダイレクトされることを確認
    def test_dashboard_requires_login(self):
        response = self.client.get(
            reverse("dashboard")
        )

        self.assertRedirects(
            response,
            reverse("login") + "?next=" + reverse("dashboard")
        )


    # 間違ったパスワードではログインできないことを確認
    def test_login_failure(self):
        logged_in = self.client.login(
            username="testuser",
            password="testpppp"
        )

        self.assertFalse(logged_in)


    # 正しいSignup情報をPOSTした場合、新しいユーザーがDBに作成されることを確認
    def test_signup_success(self):
        response = self.client.post(
            reverse("signup"),
            data={
                "username": "newuser",
                "password1": "Testpass123!",
                "password2": "Testpass123!"
            }
        )

        User = get_user_model()

        new_user = User.objects.get(
            username="newuser"
        )

        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(new_user.username, "newuser")


    # パスワードが一致しない場合、Signupに失敗しユーザーが追加されないことを確認
    def test_signup_failure(self):
        response = self.client.post(
            reverse("signup"),
            data={
                "username": "newuser",
                "password1": "Testpass123!",
                "password2": "Different123!"
            }
        )

        User = get_user_model()

        self.assertEqual(User.objects.count(), 2)


    # ログアウト後は未認証状態となり、DashboardへアクセスするとLoginへ戻されることを確認
    def test_logout(self):
        self.client.login(
            username="testuser",
            password="testpass"
        )

        self.client.logout()

        response = self.client.get(
            reverse("dashboard")
        )

        self.assertRedirects(
            response,
            reverse("login") + "?next=" + reverse("dashboard")
        )


    # ログインユーザーには自分のStudyだけが表示されることを確認
    def test_dashboard_shows_only_own_studies(self):
        Study.objects.create(
            content="Pythonを勉強する",
            user=self.user
        )

        Study.objects.create(
            content="Javaを勉強する",
            user=self.other_user
        )

        self.client.login(
            username="testuser",
            password="testpass"
        )

        response = self.client.get(
            reverse("dashboard")
        )

        # 自分のStudyは表示される
        self.assertContains(
            response,
            "Pythonを勉強する"
        )

        # 他ユーザーのStudyは表示されない
        self.assertNotContains(
            response,
            "Javaを勉強する"
        )

    # 他ユーザーのStudyは更新されない
    def test_cannot_update_other_users_study(self):
        other_study = Study.objects.create(
            content="Javaを勉強する",
            user=self.other_user
        )

        self.client.login(
            username="testuser",
            password="testpass"
        )

        response = self.client.post(
            reverse("update", args=[other_study.id]),
            data={
                "content": "勝手に書き換える"
            }
        )

        self.assertEqual(response.status_code, 404)

        other_study.refresh_from_db()

        self.assertEqual(
            other_study.content,
            "Javaを勉強する"
        )

    # 他ユーザーのStudyは削除されない
    def test_cannot_delete_other_users_study(self):
        other_study = Study.objects.create(
            content="Javaを勉強する",
            user=self.other_user
        )

        self.client.login(
            username="testuser",
            password="testpass"
        )

        response = self.client.post(
            reverse("delete", args=[other_study.id])
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(
            Study.objects.filter(id=other_study.id).exists()
        )

    # DashboardからStudyを作ったとき、ログインユーザーに正しく紐づく
    def test_create_study_for_logged_in_user(self):
        self.client.login(
            username="testuser",
            password="testpass"
        )

        response = self.client.post(
            reverse("dashboard"),
            data={
                "content": "Pythonを勉強する"
            }
        )

        self.assertEqual(Study.objects.count(), 1)

        study = Study.objects.get(
            content="Pythonを勉強する"
        )

        self.assertEqual(study.user, self.user)


    # 自分のStudyならUpdateできる
    def test_can_update_own_study(self):
        study = Study.objects.create(
            content="Pythonを勉強する",
            user=self.user
        )

        self.client.login(
            username="testuser",
            password="testpass"
        )

        response = self.client.post(
            reverse("update", args=[study.id]),
            data={
                "content": "Djangoを勉強する"
            }
        )

        study.refresh_from_db()

        self.assertEqual(
            study.content,
            "Djangoを勉強する"
        )

    # 自分のStudyならDeleteできる
    def test_can_delete_own_study(self):
        study = Study.objects.create(
            content="Pythonを勉強する",
            user=self.user
        )
        self.client.login(
            username="testuser",
            password="testpass"
        )

        self.assertEqual(Study.objects.count(), 1)

        response = self.client.post(
            reverse("delete", args=[study.id])
        )

        self.assertEqual(Study.objects.count(), 0)