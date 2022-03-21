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

웹 브라우저에서 http://127.0.0.1:8080 로 접속하여 페이지가 나온다면 정상적으로 서버 구동된 것입니다.

<br>

