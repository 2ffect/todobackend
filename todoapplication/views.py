from django.shortcuts import render

# 클래스형 view를만들기 위해서 import
from django.views import View
# csrf 설정을 위한 import
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# 데이터 모델을 가져오기 위한 import
from .models import Todo
# 날짜와 시간을 사용하기 위한 import
from datetime import datetime
# JSON으로 응답하기 위한 import
from django.http import JsonResponse
# 클라이언트의 정보를 JSON 문자열로 변환하기 위한 import
import json # python 기본 라이브러리

# 모델 클래스의 인스턴스를 딕셔너리로 변환해주는 함수 작성
# JsonResponse로 JSON 데이터를 출력 시 JSON 문자로 빠르게 변환 시키려면 JSON 문자열과 표현 방법이 같은 dict만 가능하다.
# python application 개발자가 되기 위해서는 함수를 만들 때 매개변수에 자료형을 기재하고
# return type을 기재하는 형태로 만들어주는 것이 좋다.
def todoDictionary(todo:Todo) -> dict:
    result = {
        "id" : todo.id,
        "userid" : todo.userid,
        "title" : todo.title,
        "done" : todo.done,
        "regdate" : todo.regdate,
        "moddate" : todo.moddate,
    }

# csrf 설정으로 클라이언트 애플리케이션을 별도로 구현하는 경우 필수
@method_decorator(csrf_exempt, name = 'dispatch') # 이름은 보통 dispatch 를 사용한다.
class TodoView(View):
    # POST를 처리
    def post(self,requset):
        # 클라이언트 데이터 가져오기
        # requset = json.loads(requset.data) # 에러
        requset = json.loads(requset.body)

        # 클라이언트에서 입력해주는 데이터만 읽어오면 된다.
        # userid 와 title의 매개변수 값을 읽어서 저장
        userid = requset["userid"]
        title = requset["title"]

        #모델 인스턴스 생성
        todo = Todo()
        todo.userid = userid
        todo.title = title
        
        todo.save() # 저장

        # userid 와 일치하는 데이터만 추출
        todos = Todo.objects.filter(userid = userid)

        # 결과 리턴
        # 삽입은 특별한 경우가 아니라면 데이터의 처음과 끝에 추가되기 때문에 보통 전체 데이터를 return 해도 상관없다.
        # 수정과 삭제의 경우는 테이터의 처음과 끝이 아닐수 있기 때문에 보통 수정되거나 삭제된 부분을 return 해준다.
        return JsonResponse({"list" : list(todos.values())})
    
    # GET을 처리
    def get(self, requset):
        # GET 방식에서 userid 라는 파라미터를 읽기
        userid = requset.GET["userid"]
        todos = Todo.objects.filter(userid = userid)
        return JsonResponse({"list" : list(todos.values())})
    

    # PUT을 처리
    def put(self,requset):
        # 클라이언트 데이터 가져오기
        # requset = json.loads(requset.data) # 에러
        requset = json.loads(requset.body)

        # 클라이언트에서 입력해주는 데이터만 읽어오면 된다.
        # userid 와 id그리고 done 매개변수 값을 읽어서 저장
        userid = requset["userid"]
        id = requset["id"]
        # done = requset["done"]

        # 수정할 데이터를 찾아온다
        todo = Todo.objects.get(id = id)
        # 수정할 내용을 대입
        todo.userid = userid
        # todo.id = id
        # todo.done = done
        # save는 기본키의 값이 있으면 수정이고 없으면 삽입이다.
        todo.save() # 저장

        # userid 와 일치하는 데이터만 추출
        todos = Todo.objects.filter(userid = userid)        

        return JsonResponse({"list" : list(todos.values())})
  
    # DELETE를 처리
    def delete(self,requset):
        # 클라이언트 데이터 가져오기
        # requset = json.loads(requset.data) # 에러
        requset = json.loads(requset.body)

        # 클라이언트에서 입력해주는 데이터만 읽어오면 된다.
        # userid 와 id그리고 done 매개변수 값을 읽어서 저장
        userid = requset["userid"]
        id = requset["id"]

        # 삭제할 데이터를 찾아온다
        todo = Todo.objects.get(id = id)
        # user를 확인해서 삭제
        if userid == todo.userid:
            todo.delete()

        # userid 와 일치하는 데이터만 추출
        todos = Todo.objects.filter(userid = userid)        

        return JsonResponse({"list" : list(todos.values())})