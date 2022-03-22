from django.test import TestCase
from accounts.models import User, Auth


def create_auth(phone_number):
    auth = Auth.objects.create(phone_number=phone_number)
    print('생성번호', auth.auth_number)
    return auth.auth_number


def get_auth(phone_number):
    auth = Auth.objects.get(phone_number=phone_number)
    print('조회번호', auth.auth_number)
    return auth.auth_number


def create_user(username, email, nickname, password, full_name, phone_number):
    User.objects.create_user(username=username, email=email, nickname=nickname,
                             password=password, full_name=full_name,
                             phone_number=phone_number)


class Test(TestCase):

    def test_휴대폰인증(self):
        response = self.client.post(
            '/account/auth/',

            data={
                "phone_number": "01012345678",
            }
        )
        print('출력', response)
        assert response.status_code == 200

    def test_휴대폰_검증_시_휴대폰_유효한_포맷이_아닌_경우_400_응답과_함께_관련_에러메시지가_반환(self):
        invalid_input_list = ['010581231230', '10583599891']
        for phone_number in invalid_input_list:
            response = self.client.post(
                '/account/auth/',
                data={
                    "phone_number": phone_number
                }
            )
            print('출력', response)
            print(response.json())
            assert response.status_code == 400

    def test_회원가입(self):
        auth_number = create_auth(phone_number='01012345678')

        response = self.client.post(
            '/account/signup/',
            data={
                "username": "test",
                "email": "h456522@naver.com",
                "nickname": "test",
                "password": "test",
                "full_name": "test",
                "phone_number": "01012345678",
                "auth_number": auth_number,
            }
        )
        print('결과출력', response)
        print(response.json())
        assert response.status_code == 201

    def test_식별_가능한_모든_정보로_로그인(self):
        create_user(username="test", email="h456522@naver.com", nickname="test",
                    password="test", full_name="test",
                    phone_number="01012345678")
        invalid_intpu_dictionary = {
            "username": "test",
            "email": "h456522@naver.com",
            "nickname": "test",
            "phone_number": "01012345678"
        }
        for key in invalid_intpu_dictionary:
            response = self.client.post(
                '/account/login/',
                data={
                    key: invalid_intpu_dictionary[key],
                    "password": "test"
                }
            )
            print('결과출력', response)
            print(response.json())
        assert response.status_code == 200

    def test_로그인_시_식별_가능한_모든_정보가_유효하지_않은_경우_400_응답과_함께_관련_에러메시지가_반환(self):
        create_user(username="test", email="h456522@naver.com", nickname="test",
                    password="test", full_name="test",
                    phone_number="01012345678")
        invalid_intput_dictionary = {
            "username": "test1",
            "email": "h4565221@naver.com",
            "nickname": "test1",
            "phone_number": "01012345671"
        }
        for key in invalid_intput_dictionary:
            response = self.client.post(
                '/account/login/',
                data={
                    key: invalid_intput_dictionary[key],
                    "password": "test"
                }
            )
            print('결과출력', response)
            print(response.json())
        assert response.status_code == 400

    def test_비밀번호_초기화(self):
        auth_number = create_auth(phone_number='01012345678')
        create_user(username="test", email="h456522@naver.com", nickname="test",
                    password="test", full_name="test",
                    phone_number="01012345678")
        response = self.client.post(
            '/account/change-password/',
            data={
                "phone_number": "01012345678",
                "auth_number": auth_number,
                "password": "qlalfqjsgh1",
                "password2": "qlalfqjsgh1"
            }
        )
        print('결과출력', response)
        print(response.json())
        assert response.status_code == 200
    def test_비밀번호_초기화_시_인증번호가_일치하지_않는_경우_400_응답과_함께_관련_에러메세지가_반환(self):
        auth_number = create_auth(phone_number='01012345678')
        create_user(username="test", email="h456522@naver.com", nickname="test",
                    password="test", full_name="test",
                    phone_number="01012345678")

        response = self.client.post(
            '/account/change-password/',
            data={
                "phone_number": "01012345678",
                "auth_number": "1234",
                "password": "qlalfqjsgh1",
                "password2": "qlalfqjsgh1"
            }
        )
        print('결과출력', response)
        print(response.json())
        assert response.status_code == 400

    def test_비밀번호_초기화_시_비밀번호가_일치하지_않는_경우_400_응답과_함께_관련_에러메세지가_반환(self):
        auth_number = create_auth(phone_number='01012345678')
        create_user(username="test", email="h456522@naver.com", nickname="test",
                    password="test", full_name="test",
                    phone_number="01012345678")

        response = self.client.post(
            '/account/change-password/',
            data={
                "phone_number": "01012345678",
                "auth_number": auth_number,
                "password": "qlalfqjsgh1",
                "password2": "qlalfqj"
            }
        )
        print('결과출력', response)
        print(response.json())
        assert response.status_code == 400

