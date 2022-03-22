# Account API

<br>

### 개요


계정을 관리하는 API

### 필요

- Python 3.2.x
- SQL lite3


  <br>

## 서버 구동 방법

### 로컬환경 서버 구동

1. Python 종속성 설치

```
pip install -r requirements.txt
```

​	2. DB 마이그레이션

> 설계된 모델에 대한 스키마를 데이터베이스에 반영

```bash
python manage.py migrate
```

4. 서버실행

```bash
python manage.py runserver
```

5. 서버 정상 구동 확인

웹 브라우저에서 http://127.0.0.1:8000/account/auth/ 로 접속하여 페이지가 나온다면 정상적으로 서버 구동된 것입니다.

<br>



## API Specifications

### 전화번호인증

[요청]

- URL:POST /account/auth/
- Body

```json
{
    "phone_number" : "01012345678"
}
```

[응답]

- Body

```json
{
    "auth_number": 5601
}
```

- Error

| 에러코드 | 설명                        |
| -------- | :-------------------------- |
| 400      | 파라미터 입력이 잘못된 경우 |



### 회원가입

[요청]

- URL: POST /account/signup/
- Body 파라미터 설명
  - 전화번호 인증(선행) 후 회원가입
    - auth_number: 인증받은 번호를 의미합니다. 


```json
{
    "username" : "test",
    "email" : "test@naver.com",
    "nickname" : "test",
    "password" : "test",
    "full_name" : "test",
    "phone_number" : "01012345678",
    "auth_number" : "8462"
}
```

[응답]

- Body

```json
{
    "success": "회원가입 완료"
}
```

- Error

| 에러코드 | 설명                        |
| -------- | --------------------------- |
| 400      | 파라미터 입력이 잘못된 경우 |
| 409      | 중복된 값이 입력된 경우     |



### 로그인

- [요청]

- URL: POST /account/login/

- Body

```json
{
  "username" : "username",
  "password" : "1234"
}
or
{
  "nickname" : "nickname",
  "password" : "1234"
}
or
{
  "phone_number" : "01012345678",
  "password" : "1234"
}
or
{
  "email" : "email@email.com",
  "password" : "1234"
}
```

[응답]

- Body

```json
{
  "success": "로그인성공"
}
```

- Error

| 에러코드 | 설명                          |
| -------- | ----------------------------- |
| 400      | 등록된 user가 없는 경우,      |
| 401      | Username or Password 틀릴경우 |



### 로그아웃

[요청]

- URL: POST /account/logout/

[응답]

- Body

```json
{
  "username": "test",
  "password": "1234"
} 
```

[응답]

- 응답에 대한 설명
  - 성공 응답 시 상태코드:200



### 내 정보 보기 기능

[요청]

- URL : GET /account/myinfo/:pk
  - Path 파라미터 설명 : pk 는 myinfo의 식별 아이디를 입력합니다




[응답]

- Body

```json
{
    "username": "test",
    "email": "email@naver.com",
    "nickname": "test",
    "full_name": "test",
    "phone_number": "01023456789"
} 
```

- 응답에 대한 설명

  - 성공 응답시 상태코드 : 200

  - 응답 Body 설명 : 나의 정보 결과가 반환됩니다.







### 비밀번호 재설정 기능

[요청]

- URL:POST /account/change-password/
- Body
  - 전화번호 인증 후(선행) 비밀번호 재설정


```json
{
    "phone_number" : "01023456789",
    "auth_number" : "9241",
    "password" : "password",
    "password2" : "password"
}
```

- Body 파라미터 설명
  - auth_number: 인증받은 번호를 의미합니다. 
  - password: 비밀번호를 의미합니다.

[응답]

- Body

```json
{
    "success": "비밀번호 초기화 완료"
}
```

- 응답에 대한 설명
  - 성공 응답시 상태코드 : 200
  
    

## 최종 구현된 범위

- 전화번호 인증 후 회원가입
- 식별 가능한 모든 정보로 로그인
- 내 정보 보기 기능
- 전화번호 인증 후 비밀번호 재설정



**테스트 코드**

**로그인기능** :
하나의 로그인 API에서 각각의 수단에 따른 로그인 기능을 파라메터 입력 여부에 따라 분기해서 제공.
장점: 클라이언트 & 백엔드 관리가 단일화. 로그인에 공통적인 로직을 넣기 좋다.
단점: 특정 수단에 대해서 변경하려고 할 때 사이드이팩 발생, 코드가 길어짐
단점보완: 로그인 기능별 함수 쪼개기.
